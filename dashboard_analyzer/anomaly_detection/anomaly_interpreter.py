from typing import List, Tuple, Dict, Any
from .anomaly_tree import AnomalyTree, AnomalyNode
from ..data_collection.pbi_collector import PBIDataCollector
from ..anomaly_explanation.routes_analyzer import RoutesAnalyzer
from datetime import datetime
from pathlib import Path
import pandas as pd
import asyncio

class AnomalyInterpreter:
    """
    Interprets anomaly patterns in the tree using bottom-up analysis
    following the rules defined in README.md
    """
    
    def __init__(self, pbi_collector: PBIDataCollector = None):
        self.interpretations: Dict[str, str] = {}  # node_path -> interpretation
        self.pbi_collector = pbi_collector  # For verbatims collection
        self.routes_analyzer = RoutesAnalyzer(pbi_collector) if pbi_collector else None
        self.verbatims_cache: Dict[Tuple[str, str], pd.DataFrame] = {}  # (node_path, date) -> DataFrame
        
    def analyze_node_pattern(self, parent_node: AnomalyNode, date: str, daily_anomalies: Dict[str, str]) -> str:
        """
        Analyze a parent node based on its children's anomaly states
        Returns an interpretation string following README rules
        """
        if not parent_node.children:
            return ""  # Leaf nodes don't need interpretation
            
        # Get parent and children states
        parent_path = parent_node.get_path()
        parent_state = daily_anomalies.get(parent_path, "?")
        
        children_states = []
        children_names = []
        for child_name, child_node in parent_node.children.items():
            child_path = child_node.get_path()
            child_state = daily_anomalies.get(child_path, "?")
            if child_state != "?":  # Only consider nodes with valid data
                children_states.append(child_state)
                children_names.append(child_name)
        
        if not children_states:
            return "No data available for children"
            
        # Count each type of anomaly
        normal_count = children_states.count("N")
        positive_count = children_states.count("+")
        negative_count = children_states.count("-")
        
        # Get lists of children by state
        normal_children = [name for name, state in zip(children_names, children_states) if state == "N"]
        positive_children = [name for name, state in zip(children_names, children_states) if state == "+"]
        negative_children = [name for name, state in zip(children_names, children_states) if state == "-"]
        
        # Apply README rules for interpretation
        return self._generate_interpretation(
            parent_state, 
            normal_count, positive_count, negative_count,
            normal_children, positive_children, negative_children
        )
    
    def _generate_interpretation(self, parent_state: str, 
                               normal_count: int, positive_count: int, negative_count: int,
                               normal_children: List[str], positive_children: List[str], 
                               negative_children: List[str]) -> str:
        """
        Generate interpretation text based on README rules
        """
        total_children = normal_count + positive_count + negative_count
        
        # Helper function to format child lists
        def format_children(children_list: List[str]) -> str:
            if len(children_list) == 1:
                return children_list[0]
            elif len(children_list) == 2:
                return f"{children_list[0]}, {children_list[1]}"
            else:
                return ", ".join(children_list[:-1]) + f", {children_list[-1]}"
        
        # Case 1: All children are normal
        if positive_count == 0 and negative_count == 0:
            if parent_state == "N":
                return f"All children normal ({format_children(normal_children)})"
            else:
                return f"Inconsistency: all children normal but parent is {parent_state}"
        
        # Case 2: All children are positive  
        elif normal_count == 0 and negative_count == 0:
            if parent_state == "+":
                return f"Positive anomaly consistent across all children ({format_children(positive_children)})"
            else:
                return f"Inconsistency: all children positive but parent is {parent_state}"
        
        # Case 3: All children are negative
        elif normal_count == 0 and positive_count == 0:
            if parent_state == "-":
                return f"Negative anomaly consistent across all children ({format_children(negative_children)})"
            else:
                return f"Inconsistency: all children negative but parent is {parent_state}"
        
        # Case 4: Mix of positive and negative (no normal)
        elif normal_count == 0:
            if parent_state == "N":
                return f"Positive nodes ({format_children(positive_children)}) cancel with negative nodes ({format_children(negative_children)})"
            elif parent_state == "+":
                return f"Positive nodes ({format_children(positive_children)}) outweigh negative nodes ({format_children(negative_children)})"
            elif parent_state == "-":
                return f"Negative nodes ({format_children(negative_children)}) outweigh positive nodes ({format_children(positive_children)})"
        
        # Case 5: Mix of normal and positive (no negative)
        elif negative_count == 0:
            if parent_state == "N":
                return f"Positive nodes ({format_children(positive_children)}) diluted by normal nodes ({format_children(normal_children)})"
            elif parent_state == "+":
                return f"Positive nodes ({format_children(positive_children)}) significant despite normal nodes ({format_children(normal_children)})"
            else:
                return f"Inconsistency: positive and normal children but parent is {parent_state}"
        
        # Case 6: Mix of normal and negative (no positive)
        elif positive_count == 0:
            if parent_state == "N":
                return f"Negative nodes ({format_children(negative_children)}) diluted by normal nodes ({format_children(normal_children)})"
            elif parent_state == "-":
                return f"Negative nodes ({format_children(negative_children)}) significant despite normal nodes ({format_children(normal_children)})"
            else:
                return f"Inconsistency: negative and normal children but parent is {parent_state}"
        
        # Case 7: Mix of all three types
        else:
            if parent_state == "N":
                return f"Mixed anomalies: positive ({format_children(positive_children)}), negative ({format_children(negative_children)}), normal ({format_children(normal_children)}) balance out"
            elif parent_state == "+":
                return f"Positive nodes ({format_children(positive_children)}) dominate over negative ({format_children(negative_children)}) and normal ({format_children(normal_children)})"
            elif parent_state == "-":
                return f"Negative nodes ({format_children(negative_children)}) dominate over positive ({format_children(positive_children)}) and normal ({format_children(normal_children)})"
        
        return "Unable to interpret pattern"
    
    def analyze_tree_for_date(self, tree: AnomalyTree, date: str) -> Dict[str, str]:
        """
        Perform bottom-up analysis for all parent nodes on a specific date
        Returns dictionary of node_path -> interpretation
        """
        if date not in tree.daily_anomalies:
            return {}
            
        interpretations = {}
        daily_anomalies = tree.daily_anomalies[date]
        
        # Bottom-up analysis: start from deepest nodes and work up
        # We'll process nodes in reverse order of their depth
        nodes_by_depth = {}
        
        for node_path, node in tree.nodes.items():
            depth = len(node_path.split('/')) - 1  # -1 because Global is depth 0
            if depth not in nodes_by_depth:
                nodes_by_depth[depth] = []
            nodes_by_depth[depth].append((node_path, node))
        
        # Process from deepest to shallowest
        max_depth = max(nodes_by_depth.keys()) if nodes_by_depth else 0
        
        for depth in range(max_depth, -1, -1):
            if depth in nodes_by_depth:
                for node_path, node in nodes_by_depth[depth]:
                    if node.children:  # Only process parent nodes
                        interpretation = self.analyze_node_pattern(node, date, daily_anomalies)
                        if interpretation:
                            interpretations[node_path] = interpretation
        
        self.interpretations = interpretations
        return interpretations
    
    def print_interpreted_tree(self, tree: AnomalyTree, date: str, interpretations: Dict[str, str] = None):
        """
        Print the tree with interpretations, NPS values, and explanation flags for a specific date
        """
        if interpretations is None:
            interpretations = self.analyze_tree_for_date(tree, date)
            
        if date not in tree.daily_anomalies:
            print(f"❌ No anomaly data for date: {date}")
            return
            
        print(f"\n🌳 Anomaly Tree: {date}")
        print("-" * 50)
        
        anomalies = tree.daily_anomalies[date]
        
        # Helper function to get NPS values and delta
        def get_nps_info(node_path: str) -> str:
            if node_path in tree.nodes:
                node = tree.nodes[node_path]
                if hasattr(node, 'daily_nps') and date in node.daily_nps:
                    daily_nps = node.daily_nps[date]
                    if hasattr(node, 'moving_averages') and date in node.moving_averages:
                        ma = node.moving_averages[date]
                        delta = daily_nps - ma
                        return f"  Daily NPS: {daily_nps:.1f} vs MA: {ma:.1f} (Δ: {delta:+.1f})"
                    else:
                        return f"  Daily NPS: {daily_nps:.1f} (No MA data)"
            return ""
        
        # Helper function to check if explanation is needed
        def needs_explanation_tag(node_path: str) -> str:
            node_state = anomalies.get(node_path, "?")
            if node_state not in ["+", "-"]:
                return ""  # Only anomalous nodes need explanation
                
            # Get the level and parent path
            path_parts = node_path.split('/')
            if len(path_parts) <= 1:
                return " [Explanation needed]"  # Root level anomaly always needs explanation
                
            parent_path = '/'.join(path_parts[:-1])
            current_level = len(path_parts)
            
            # Find all siblings (nodes with same parent)
            siblings = []
            siblings_with_anomaly = []
            siblings_with_same_anomaly = []
            
            for other_path, other_state in anomalies.items():
                other_parts = other_path.split('/')
                if (len(other_parts) == current_level and 
                    '/'.join(other_parts[:-1]) == parent_path and
                    other_path != node_path):
                    siblings.append((other_path, other_state))
                    if other_state in ["+", "-"]:
                        siblings_with_anomaly.append((other_path, other_state))
                        if other_state == node_state:
                            siblings_with_same_anomaly.append((other_path, other_state))
            
            # Apply README logic:
            # 1. Isolated anomaly: this is the only child with any anomaly
            # 2. Homogeneous anomaly: 2+ children (including self) have same anomaly type
            
            total_with_same_anomaly = len(siblings_with_same_anomaly) + 1  # +1 for self
            total_with_any_anomaly = len(siblings_with_anomaly) + 1  # +1 for self
            
            # Case 1: Isolated anomaly (only this child has any anomaly)
            if total_with_any_anomaly == 1:
                return " [Explanation needed]"
                
            # Case 2: Homogeneous anomaly (2+ children have same anomaly)
            if total_with_same_anomaly >= 2:
                return " [Explanation needed]"
                
            # Case 3: Mixed anomalies (siblings have different anomaly types)
            # In this case, each anomaly is considered isolated within its type
            return " [Explanation needed]"
        
        # Print Global node
        global_state = anomalies.get("Global", "?")
        global_interpretation = interpretations.get("Global", "")
        global_nps_info = get_nps_info("Global")
        print(f"Global [{global_state}]{needs_explanation_tag('Global')}")
        if global_nps_info:
            print(global_nps_info)
        if global_interpretation:
            print(f"  {global_interpretation}")
        
        # Print LH branch
        lh_state = anomalies.get("Global/LH", "?")
        lh_interpretation = interpretations.get("Global/LH", "")
        lh_nps_info = get_nps_info("Global/LH")
        print(f"  LH [{lh_state}]{needs_explanation_tag('Global/LH')}")
        if lh_nps_info:
            print(f"  {lh_nps_info}")
        if lh_interpretation:
            print(f"    {lh_interpretation}")
        
        lh_cabins = ["Economy", "Business", "Premium"]
        for cabin in lh_cabins:
            cabin_path = f"Global/LH/{cabin}"
            cabin_state = anomalies.get(cabin_path, "?")
            cabin_interpretation = interpretations.get(cabin_path, "")
            cabin_nps_info = get_nps_info(cabin_path)
            print(f"    {cabin} [{cabin_state}]{needs_explanation_tag(cabin_path)}")
            if cabin_nps_info:
                print(f"    {cabin_nps_info}")
            if cabin_interpretation:
                print(f"      {cabin_interpretation}")
        
        # Print SH branch
        sh_state = anomalies.get("Global/SH", "?")
        sh_interpretation = interpretations.get("Global/SH", "")
        sh_nps_info = get_nps_info("Global/SH")
        print(f"  SH [{sh_state}]{needs_explanation_tag('Global/SH')}")
        if sh_nps_info:
            print(f"  {sh_nps_info}")
        if sh_interpretation:
            print(f"    {sh_interpretation}")
        
        sh_cabins = ["Economy", "Business"]
        for cabin in sh_cabins:
            cabin_path = f"Global/SH/{cabin}"
            cabin_state = anomalies.get(cabin_path, "?")
            cabin_interpretation = interpretations.get(cabin_path, "")
            cabin_nps_info = get_nps_info(cabin_path)
            print(f"    {cabin} [{cabin_state}]{needs_explanation_tag(cabin_path)}")
            if cabin_nps_info:
                print(f"    {cabin_nps_info}")
            if cabin_interpretation:
                print(f"      {cabin_interpretation}")
            
            # Company subdivisions for SH
            companies = ["IB", "YW"]
            for company in companies:
                company_path = f"Global/SH/{cabin}/{company}"
                company_state = anomalies.get(company_path, "?")
                company_interpretation = interpretations.get(company_path, "")
                company_nps_info = get_nps_info(company_path)
                print(f"      {company} [{company_state}]{needs_explanation_tag(company_path)}")
                if company_nps_info:
                    print(f"      {company_nps_info}")
                if company_interpretation:
                    print(f"        {company_interpretation}")
    
    def analyze_week_interpretations(self, tree: AnomalyTree, dates: List[str]) -> Dict[str, Dict[str, str]]:
        """
        Analyze interpretations for multiple dates
        Returns dict of date -> {node_path -> interpretation}
        """
        week_interpretations = {}
        
        for date in dates:
            week_interpretations[date] = self.analyze_tree_for_date(tree, date)
            
        return week_interpretations
    
    def _needs_explanation(self, node_path: str, anomaly_state: str, parent_node: AnomalyNode, 
                          daily_anomalies: Dict[str, str]) -> bool:
        """
        Determine if a node needs explanation based on README rules:
        - Isolated anomalies (single child with anomaly): need explanation
        - Homogeneous anomalies (2+ children with same anomaly): need explanation to determine if common cause
        """
        if anomaly_state in ["N", "?"]:
            return False  # Normal nodes don't need explanation
            
        # Check if this is a leaf node (always needs explanation if anomalous)
        if not hasattr(parent_node, 'children') or not parent_node.children:
            return True
            
        # Get parent node to analyze siblings
        # Find the parent of this node
        path_parts = node_path.split('/')
        if len(path_parts) <= 1:
            return True  # Root node anomaly always needs explanation
            
        # Count siblings with same anomaly state
        siblings_with_same_anomaly = 0
        total_siblings = 0
        
        # We need to look at the parent of this node to see its siblings
        parent_path = '/'.join(path_parts[:-1])
        
        # Find the parent node in the tree structure
        # This is a bit complex since we need to navigate the tree
        # For now, let's use a simpler approach: check if there are other nodes at same level with same anomaly
        same_level_nodes = []
        current_level = len(path_parts)
        
        for other_path, other_state in daily_anomalies.items():
            other_parts = other_path.split('/')
            if (len(other_parts) == current_level and 
                '/'.join(other_parts[:-1]) == '/'.join(path_parts[:-1])):  # Same parent
                same_level_nodes.append((other_path, other_state))
                total_siblings += 1
                if other_state == anomaly_state:
                    siblings_with_same_anomaly += 1
        
        # Apply README logic:
        # 1. Isolated anomaly (only this child has anomaly): needs explanation
        # 2. Homogeneous anomaly (2+ children with same anomaly): needs explanation
        if siblings_with_same_anomaly == 1:
            return True  # Isolated anomaly
        elif siblings_with_same_anomaly >= 2:
            return True  # Homogeneous anomaly (could be common cause or coincidence)
            
        return False
    
    def print_propagation_analysis(self, tree: AnomalyTree, date: str, interpretations: Dict[str, str] = None):
        """
        Print the propagation analysis (original format without NPS values)
        """
        if interpretations is None:
            interpretations = self.analyze_tree_for_date(tree, date)
            
        if date not in tree.daily_anomalies:
            print(f"❌ No anomaly data for date: {date}")
            return
            
        print(f"\n🔍 Anomaly Propagation Analysis: {date}")
        print("-" * 50)
        
        anomalies = tree.daily_anomalies[date]
        
        # Print Global node
        global_state = anomalies.get("Global", "?")
        global_interpretation = interpretations.get("Global", "")
        print(f"Global [{global_state}]")
        if global_interpretation:
            print(f"  {global_interpretation}")
        
        # Print LH branch
        lh_state = anomalies.get("Global/LH", "?")
        lh_interpretation = interpretations.get("Global/LH", "")
        print(f"  LH [{lh_state}]")
        if lh_interpretation:
            print(f"    {lh_interpretation}")
        
        lh_cabins = ["Economy", "Business", "Premium"]
        for cabin in lh_cabins:
            cabin_path = f"Global/LH/{cabin}"
            cabin_state = anomalies.get(cabin_path, "?")
            cabin_interpretation = interpretations.get(cabin_path, "")
            print(f"    {cabin} [{cabin_state}]")
            if cabin_interpretation:
                print(f"      {cabin_interpretation}")
        
        # Print SH branch
        sh_state = anomalies.get("Global/SH", "?")
        sh_interpretation = interpretations.get("Global/SH", "")
        print(f"  SH [{sh_state}]")
        if sh_interpretation:
            print(f"    {sh_interpretation}")
        
        sh_cabins = ["Economy", "Business"]
        for cabin in sh_cabins:
            cabin_path = f"Global/SH/{cabin}"
            cabin_state = anomalies.get(cabin_path, "?")
            cabin_interpretation = interpretations.get(cabin_path, "")
            print(f"    {cabin} [{cabin_state}]")
            if cabin_interpretation:
                print(f"      {cabin_interpretation}")
            
            # Company subdivisions for SH
            companies = ["IB", "YW"]
            for company in companies:
                company_path = f"Global/SH/{cabin}/{company}"
                company_state = anomalies.get(company_path, "?")
                company_interpretation = interpretations.get(company_path, "")
                print(f"      {company} [{company_state}]")
                if company_interpretation:
                    print(f"        {company_interpretation}")

    def print_tree_with_operational_explanations(self, tree: AnomalyTree, date: str, 
                                                operational_analyzer, interpretations: Dict[str, str] = None,
                                                routes_data: Dict[str, List[Dict]] = None):
        """
        Print the anomaly tree with enhanced formatting and clearer explanations
        """
        if interpretations is None:
            interpretations = self.analyze_tree_for_date(tree, date)
            
        if date not in tree.daily_anomalies:
            print(f"❌ No anomaly data for date: {date}")
            return
            
        print(f"\n🌳 ANOMALY ANALYSIS TREE: {date}")
        print("="*70)
        
        anomalies = tree.daily_anomalies[date]
        
        # Helper function to format explanations clearly
        def format_explanations(node_path: str, indent: str = "") -> str:
            node_state = anomalies.get(node_path, "?")
            if node_state not in ["+", "-"]:
                return ""
                
            anomaly_type = "positive" if node_state == "+" else "negative"
            explanations = operational_analyzer.get_specific_explanations(node_path, date, anomaly_type)
            
            result_lines = []
            
            # Operational factors
            if explanations['otp_explanation'] != "No OTP data available":
                result_lines.append(f"{indent}  ✈️  On-Time Performance: {explanations['otp_explanation']}")
            if explanations['load_factor_explanation'] != "No Load Factor data available":
                result_lines.append(f"{indent}  👥 Load Factor: {explanations['load_factor_explanation']}")
            
            # Routes information
            if routes_data and node_path in routes_data:
                routes_explanation = self.routes_analyzer.format_routes_explanation(
                    routes_data[node_path], node_state
                )
                if routes_explanation:
                    result_lines.append(f"{indent}  🛣️  {routes_explanation}")
            
            # Customer feedback
            if hasattr(self, 'verbatims_cache'):
                cache_key = (node_path, date)
                if cache_key in self.verbatims_cache:
                    verbatims_df = self.verbatims_cache[cache_key]
                    verbatims_explanation = self.analyze_verbatims_sentiment_by_topic(verbatims_df, anomaly_type)
                    if verbatims_explanation and "No verbatims" not in verbatims_explanation:
                        result_lines.append(f"{indent}  💬 Customer Feedback: {verbatims_explanation}")
            
            return "\n" + "\n".join(result_lines) if result_lines else ""
        
        # Print the tree structure with clear hierarchy
        
        # 1. GLOBAL LEVEL
        global_state = anomalies.get("Global", "?")
        global_interpretation = interpretations.get("Global", "")
        print(f"\n🌍 GLOBAL [{global_state}]")
        if global_interpretation:
            print(f"   📊 Pattern Analysis: {global_interpretation}")
        print(format_explanations("Global"))
        
        # 2. HAUL TYPES
        print(f"\n┌─ 🛫 LONG HAUL (LH) [{anomalies.get('Global/LH', '?')}]")
        lh_interpretation = interpretations.get("Global/LH", "")
        if lh_interpretation:
            print(f"│    📊 Pattern Analysis: {lh_interpretation}")
        print(format_explanations("Global/LH", "│"))
        
        # 2.1 LH Cabin Classes
        lh_cabins = ["Economy", "Business", "Premium"]
        for i, cabin in enumerate(lh_cabins):
            cabin_path = f"Global/LH/{cabin}"
            cabin_state = anomalies.get(cabin_path, "?")
            cabin_interpretation = interpretations.get(cabin_path, "")
            
            connector = "├──" if i < len(lh_cabins) - 1 else "└──"
            print(f"│  {connector} 💺 {cabin} [{cabin_state}]")
            if cabin_interpretation:
                print(f"│      📊 Pattern Analysis: {cabin_interpretation}")
            explanations = format_explanations(cabin_path, "│  ")
            if explanations:
                print(explanations)
        
        print(f"\n└─ ✈️  SHORT HAUL (SH) [{anomalies.get('Global/SH', '?')}]")
        sh_interpretation = interpretations.get("Global/SH", "")
        if sh_interpretation:
            print(f"     📊 Pattern Analysis: {sh_interpretation}")
        print(format_explanations("Global/SH", " "))
        
        # 2.2 SH Cabin Classes and Companies
        sh_cabins = ["Economy", "Business"]
        for i, cabin in enumerate(sh_cabins):
            cabin_path = f"Global/SH/{cabin}"
            cabin_state = anomalies.get(cabin_path, "?")
            cabin_interpretation = interpretations.get(cabin_path, "")
            
            connector = "├──" if i < len(sh_cabins) - 1 else "└──"
            print(f"   {connector} 💺 {cabin} [{cabin_state}]")
            if cabin_interpretation:
                print(f"   │    📊 Pattern Analysis: {cabin_interpretation}")
            explanations = format_explanations(cabin_path, "   │")
            if explanations:
                print(explanations)
            
            # Companies for each SH cabin
            companies = ["IB", "YW"]
            for j, company in enumerate(companies):
                company_path = f"Global/SH/{cabin}/{company}"
                company_state = anomalies.get(company_path, "?")
                company_interpretation = interpretations.get(company_path, "")
                
                comp_connector = "├──" if j < len(companies) - 1 else "└──"
                symbol = "├──" if i < len(sh_cabins) - 1 else "   "
                print(f"   {symbol} │  {comp_connector} 🏢 {company} [{company_state}]")
                if company_interpretation:
                    print(f"   {symbol} │      📊 Pattern Analysis: {company_interpretation}")
                explanations = format_explanations(company_path, f"   {symbol} │  ")
                if explanations:
                    print(explanations)
        
        print("="*70)

    def analyze_verbatims_sentiment_by_topic(self, verbatims_df: pd.DataFrame, anomaly_type: str) -> str:
        """
        Analyze verbatims sentiment by topic and return explanation based on anomaly type
        """
        if verbatims_df.empty:
            return "No verbatims data available for sentiment analysis"
        
        # Check if required columns exist
        if 'verbatims_sentiment[topic]' not in verbatims_df.columns or 'verbatims_sentiment[sentiment]' not in verbatims_df.columns:
            return "Verbatims data missing required sentiment/topic columns"
        
        # Get sentiment and topic columns
        topic_col = 'verbatims_sentiment[topic]'
        sentiment_col = 'verbatims_sentiment[sentiment]'
        
        # Filter based on anomaly type
        target_sentiment = "Negative" if anomaly_type == "negative" else "Positive"
        filtered_verbatims = verbatims_df[verbatims_df[sentiment_col] == target_sentiment]
        
        if filtered_verbatims.empty:
            return f"No {target_sentiment.lower()} verbatims found"
        
        # Count by topic
        topic_counts = filtered_verbatims[topic_col].value_counts()
        
        if topic_counts.empty:
            return f"No {target_sentiment.lower()} verbatims by topic found"
        
        # Get top topic and total count
        top_topic = topic_counts.index[0]
        top_count = topic_counts.iloc[0]
        total_verbatims = len(filtered_verbatims)
        
        # Build explanation
        explanation = f"Verbatims: {total_verbatims} {target_sentiment.lower()} feedback"
        
        if len(topic_counts) > 1:
            # Multiple topics
            explanation += f", top issue: '{top_topic}' ({top_count} mentions)"
            if len(topic_counts) > 2:
                second_topic = topic_counts.index[1]
                second_count = topic_counts.iloc[1]
                explanation += f", followed by '{second_topic}' ({second_count})"
        else:
            # Single topic
            explanation += f" focused on '{top_topic}' ({top_count} mentions)"
        
        return explanation

    def collect_verbatims_for_explanation_needed(self, tree: AnomalyTree, date: str, 
                                               output_dir: Path = None) -> Dict[str, pd.DataFrame]:
        """
        Collect verbatims for all nodes that have "explanation needed" flags for a specific date
        Returns dict of node_path -> verbatims DataFrame
        """
        if not self.pbi_collector:
            print("❌ No PBI collector available for verbatims collection")
            return {}
        
        if date not in tree.daily_anomalies:
            print(f"❌ No anomaly data for date: {date}")
            return {}
            
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        anomalies = tree.daily_anomalies[date]
        verbatims_collected = {}
        
        print(f"\n📝 COLLECTING VERBATIMS FOR EXPLANATION NEEDED FLAGS: {date}")
        print("="*70)
        
        # Check each node for explanation needed
        for node_path, node_state in anomalies.items():
            if self._node_needs_verbatims_explanation(node_path, node_state, anomalies):
                print(f"🔍 {node_path} [{node_state}] - collecting verbatims...")
                
                # Check cache first
                cache_key = (node_path, date)
                if cache_key in self.verbatims_cache:
                    verbatims_df = self.verbatims_cache[cache_key]
                    print(f"  📋 Using cached verbatims ({len(verbatims_df)} rows)")
                else:
                    # Collect fresh verbatims
                    verbatims_df = self.pbi_collector.collect_verbatims_for_date_and_segment(
                        node_path, date_obj, output_dir
                    )
                    # Cache the result
                    self.verbatims_cache[cache_key] = verbatims_df
                
                if not verbatims_df.empty:
                    verbatims_collected[node_path] = verbatims_df
                    # Show brief summary
                    anomaly_type = "negative" if node_state == "-" else "positive"
                    sentiment_summary = self.analyze_verbatims_sentiment_by_topic(verbatims_df, anomaly_type)
                    if sentiment_summary and "No verbatims" not in sentiment_summary:
                        print(f"  ✅ {len(verbatims_df)} verbatims - {sentiment_summary}")
                    else:
                        print(f"  ✅ {len(verbatims_df)} verbatims collected")
                else:
                    print(f"  ❌ No verbatims found")
        
        if verbatims_collected:
            print(f"\n✅ Verbatims collection completed: {len(verbatims_collected)} nodes with data")
        else:
            print(f"\n⚠️  No verbatims collected (no explanation needed flags or no data)")
            
        return verbatims_collected

    def _node_needs_verbatims_explanation(self, node_path: str, node_state: str, daily_anomalies: Dict[str, str]) -> bool:
        """
        Simplified check for verbatims collection - any anomalous node needs verbatims
        """
        return node_state in ["+", "-"]

    async def collect_routes_for_explanation_needed(self, tree: AnomalyTree, date: str) -> Dict[str, List[Dict]]:
        """
        Collect route data for all nodes that have "explanation needed" flags for a specific date
        Returns dict of node_path -> list of route info
        """
        if not self.routes_analyzer:
            print("❌ No routes analyzer available for routes collection")
            return {}
        
        if date not in tree.daily_anomalies:
            print(f"❌ No anomaly data for date: {date}")
            return {}
            
        anomalies = tree.daily_anomalies[date]
        routes_collected = {}
        
        print(f"\n📍 COLLECTING ROUTES DATA FOR EXPLANATION NEEDED FLAGS: {date}")
        print("="*70)
        
        # Load routes data for this date (only once)
        node_paths_with_explanations = [
            node_path for node_path, node_state in anomalies.items() 
            if self._node_needs_verbatims_explanation(node_path, node_state, anomalies)
        ]
        
        if node_paths_with_explanations:
            await self.routes_analyzer.load_routes_data(date, node_paths_with_explanations)
        
        # Check each node for explanation needed and collect routes
        for node_path, node_state in anomalies.items():
            if self._node_needs_verbatims_explanation(node_path, node_state, anomalies):
                print(f"🔍 {node_path} [{node_state}] - analyzing routes...")
                
                # Get most affected routes for this segment
                top_routes = self.routes_analyzer.get_most_affected_routes(
                    date, node_path, node_state, top_n=3
                )
                
                if top_routes:
                    routes_collected[node_path] = top_routes
                    # Format route explanation
                    routes_explanation = self.routes_analyzer.format_routes_explanation(top_routes, node_state)
                    print(f"  ✅ {len(top_routes)} routes analyzed - {routes_explanation}")
                else:
                    print(f"  ❌ No routes data available for {node_path}")
        
        if not routes_collected:
            print("⚠️  No routes data collected (no explanation needed flags or no data)")
        else:
            print(f"✅ Routes collection completed: {len(routes_collected)} nodes with data")
        
        return routes_collected 