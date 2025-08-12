"""
Flexible Anomaly Detection System
Supports different temporal aggregation periods (7 days, 14 days, 30 days, etc.)
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

class AnomalyNode:
    """Represents a node in the anomaly detection tree"""
    
    def __init__(self, name: str, path: str, parent=None):
        self.name = name
        self.path = path
        self.parent = parent
        self.children: Dict[str, 'AnomalyNode'] = {}
        self.data: Optional[pd.DataFrame] = None
        self.moving_averages: Dict[str, float] = {}  # day_of_week -> moving_average
        self.daily_anomaly: Optional['Anomaly'] = None
        self.weekly_anomaly: Optional['Anomaly'] = None
        self.explanation: Optional[str] = None
        self.insufficient_sample: bool = False  # Flag for insufficient sample size
        self.insufficient_sample_dates: set = set()  # Set to track dates with insufficient sample
        
    def add_child(self, child: 'AnomalyNode'):
        """Add a child node"""
        self.children[child.name] = child
        child.parent = self
        
    def get_path(self) -> str:
        """Get the full path of this node"""
        return self.path
        
    def is_leaf(self) -> bool:
        """Check if this is a leaf node"""
        return len(self.children) == 0
        
    def get_all_descendants(self) -> List['AnomalyNode']:
        """Get all descendant nodes"""
        descendants = []
        for child in self.children.values():
            descendants.append(child)
            descendants.extend(child.get_all_descendants())
        return descendants

class Anomaly:
    """Represents an anomaly detection result"""
    
    def __init__(self, current_value: float, target_value: float, 
                 deviation: float, threshold: float, anomaly_type: str):
        self.current_value = current_value
        self.target_value = target_value
        self.deviation = deviation
        self.threshold = threshold
        self.anomaly_type = anomaly_type  # 'daily' or 'weekly'
        self.is_anomaly = abs(deviation) > threshold

class AnomalyTree:
    """Tree structure for anomaly detection across hierarchical nodes"""
    
    def __init__(self, data_base_path: str = "tables"):
        self.data_base_path = Path(data_base_path)
        self.root: Optional[AnomalyNode] = None
        self.nodes: Dict[str, AnomalyNode] = {}
        self.dates: List[str] = []
        
    def build_tree_structure(self):
        """Build the tree structure based on the README hierarchy"""
        # Create root node
        self.root = AnomalyNode("Global", "Global")
        self.nodes["Global"] = self.root
        
        # Create LH branch (only goes to cabin level)
        lh_node = AnomalyNode("LH", "Global/LH", self.root)
        self.root.add_child(lh_node)
        self.nodes["Global/LH"] = lh_node
        
        # LH cabin nodes (no company subdivision)
        for cabin in ["Economy", "Business", "Premium"]:
            cabin_node = AnomalyNode(cabin, f"Global/LH/{cabin}", lh_node)
            lh_node.add_child(cabin_node)
            self.nodes[f"Global/LH/{cabin}"] = cabin_node
            
        # Create SH branch (goes to cabin AND company level)
        sh_node = AnomalyNode("SH", "Global/SH", self.root)
        self.root.add_child(sh_node)
        self.nodes["Global/SH"] = sh_node
        
        # SH cabin nodes with company subdivisions
        for cabin in ["Economy", "Business"]:
            cabin_node = AnomalyNode(cabin, f"Global/SH/{cabin}", sh_node)
            sh_node.add_child(cabin_node)
            self.nodes[f"Global/SH/{cabin}"] = cabin_node
            
            # Add company subdivisions for SH
            for company in ["IB", "YW"]:
                company_node = AnomalyNode(company, f"Global/SH/{cabin}/{company}", cabin_node)
                cabin_node.add_child(company_node)
                self.nodes[f"Global/SH/{cabin}/{company}"] = company_node
                
    def load_data(self, date_folder: str = "22_05_2025"):
        """Load NPS data for all nodes from the specified date folder"""
        data_path = self.data_base_path / date_folder
        
        if not data_path.exists():
            raise FileNotFoundError(f"Data folder not found: {data_path}")
            
        print(f"📊 Loading data from: {data_path}")
        
        # Load data for each node
        loaded_nodes = 0
        for node_path, node in self.nodes.items():
            nps_file = data_path / node_path / "daily_NPS.csv"
            
            if nps_file.exists():
                try:
                    df = pd.read_csv(nps_file)
                    if not df.empty:
                        # Fix column names to match actual CSV structure
                        df = df.rename(columns={
                            'Date_Master[Date]': 'Date',
                            '[NPS_Raw]': 'NPS',
                            '[Responses]': 'Responses',
                            '[Target]': 'Target'
                        })
                        
                        # Ensure Date column is datetime
                        df['Date'] = pd.to_datetime(df['Date'])
                        df = df.sort_values('Date')
                        node.data = df
                        loaded_nodes += 1
                        
                        # Update global dates list
                        if not self.dates:
                            self.dates = df['Date'].dt.strftime('%Y-%m-%d').tolist()
                            
                except Exception as e:
                    print(f"⚠️ Error loading data for {node_path}: {e}")
                    
        print(f"✅ Loaded data for {loaded_nodes}/{len(self.nodes)} nodes")
        print(f"📅 Date range: {len(self.dates)} days ({self.dates[0]} to {self.dates[-1]})")
        
    def calculate_moving_averages(self, window_days: int = 7):
        """Calculate mean of last 7 days for each node"""
        print(f"📈 Calculating mean of last {window_days} days...")
        
        for node_path, node in self.nodes.items():
            if node.data is not None and len(node.data) >= window_days:
                # Get the last 7 days of data
                last_7_days = node.data.tail(window_days)
                
                # Calculate the mean of these last 7 days
                mean_last_7_days = last_7_days['NPS'].mean()
                
                # Store this mean for later comparison
                node.data['mean_last_7_days'] = mean_last_7_days
                
    def detect_daily_anomalies(self, threshold: float = 5.0, min_sample_size: int = 5):
        """Detect anomalies for each of the last 7 days comparing with their mean"""
        print(f"🔍 Detecting anomalies in last 7 days (threshold: ±{threshold} points, min sample: {min_sample_size} responses)...")
        
        # Dictionary to store anomaly states for each day
        self.daily_anomalies: Dict[str, Dict[str, str]] = {}  # date -> {node_path -> anomaly_state}
        
        # Only analyze the last 7 days
        last_7_dates = self.dates[-7:] if len(self.dates) >= 7 else self.dates
        
        for date in last_7_dates:
            self.daily_anomalies[date] = {}
            
            for node_path, node in self.nodes.items():
                if node.data is not None and hasattr(node.data, 'mean_last_7_days'):
                    # Find data for this specific date
                    day_data = node.data[node.data['Date'].dt.strftime('%Y-%m-%d') == date]
                    
                    if not day_data.empty:
                        current_nps = day_data.iloc[0]['NPS']
                        responses = day_data.iloc[0]['Responses'] if 'Responses' in day_data.columns else 0
                        
                        # Check minimum sample size
                        if responses < min_sample_size:
                            self.daily_anomalies[date][node_path] = "S"  # S = insufficient Sample
                            # Mark the node as having insufficient sample for this date
                            if not hasattr(node, 'insufficient_sample_dates'):
                                node.insufficient_sample_dates = set()
                            node.insufficient_sample_dates.add(date)
                        else:
                            mean_last_7_days = node.data['mean_last_7_days'].iloc[0]  # This is the same for all rows
                            deviation = current_nps - mean_last_7_days
                            
                            # Determine anomaly state based on README criteria
                            if deviation >= threshold:
                                anomaly_state = "+"
                            elif deviation <= -threshold:
                                anomaly_state = "-"
                            else:
                                anomaly_state = "N"
                                
                            self.daily_anomalies[date][node_path] = anomaly_state
                    else:
                        # No data for this date
                        self.daily_anomalies[date][node_path] = "?"
                else:
                    # No data or insufficient history
                    self.daily_anomalies[date][node_path] = "?"
        
    def print_collapsed_tree(self, date: str):
        """Print collapsed tree view for a specific date"""
        if date not in self.daily_anomalies:
            print(f"❌ No anomaly data for date: {date}")
            return
            
        print(f"\n🌳 Anomaly Tree for {date}")
        print("=" * 40)
        
        anomalies = self.daily_anomalies[date]
        
        # Print in hierarchical format
        global_state = anomalies.get("Global", "?")
        print(f"Global [{global_state}]")
        
        # LH branch
        lh_state = anomalies.get("Global/LH", "?")
        print(f"├── LH [{lh_state}]")
        
        lh_cabins = ["Economy", "Business", "Premium"]
        for i, cabin in enumerate(lh_cabins):
            cabin_path = f"Global/LH/{cabin}"
            cabin_state = anomalies.get(cabin_path, "?")
            prefix = "    ├──" if i < len(lh_cabins) - 1 else "    └──"
            print(f"{prefix} {cabin} [{cabin_state}]")
            
        # SH branch  
        sh_state = anomalies.get("Global/SH", "?")
        print(f"└── SH [{sh_state}]")
        
        sh_cabins = ["Economy", "Business"]
        for i, cabin in enumerate(sh_cabins):
            cabin_path = f"Global/SH/{cabin}"
            cabin_state = anomalies.get(cabin_path, "?")
            prefix = "    ├──" if i < len(sh_cabins) - 1 else "    └──"
            print(f"{prefix} {cabin} [{cabin_state}]")
            
            # Add company subdivisions for SH
            companies = ["IB", "YW"]
            for j, company in enumerate(companies):
                company_path = f"Global/SH/{cabin}/{company}"
                company_state = anomalies.get(company_path, "?")
                company_prefix = "        ├──" if j < len(companies) - 1 else "        └──"
                print(f"{company_prefix} {company} [{company_state}]")
                
    def print_all_days_summary(self):
        """Print anomaly summary for the last 7 days"""
        print(f"\n📊 ANOMALY DETECTION SUMMARY (Last 7 Days)")
        print("=" * 60)
        print("Legend: [+] Above 7-day mean +5pts | [-] Below 7-day mean -5pts | [N] Normal | [S] Insufficient sample (<5) | [?] No data")
        print()
        
        # Only show dates that we analyzed (last 7 days)
        analyzed_dates = sorted(self.daily_anomalies.keys())
        
        for date in analyzed_dates:
            if date in self.daily_anomalies:
                # Count anomalies for this day
                anomalies = self.daily_anomalies[date]
                plus_count = sum(1 for state in anomalies.values() if state == "+")
                minus_count = sum(1 for state in anomalies.values() if state == "-")
                normal_count = sum(1 for state in anomalies.values() if state == "N")
                sample_count = sum(1 for state in anomalies.values() if state == "S")
                no_data_count = sum(1 for state in anomalies.values() if state == "?")
                total_count = len(anomalies)
                
                # Determine overall status
                if plus_count > 0 or minus_count > 0:
                    status = "🚨 Alert"
                else:
                    status = "✅ Normal"
                
                print(f"{date}   {status:<12} +{plus_count:2d} -{minus_count:2d} N{normal_count:2d} S{sample_count:2d} ?{no_data_count:2d} Total:{total_count:2d}")
        
        print("-" * 60)
        
    def analyze_date(self, date: str):
        """Analyze anomalies for a specific date and generate explanations"""
        if date not in self.daily_anomalies:
            print(f"❌ No anomaly data for date: {date}")
            return
            
        print(f"\n🔍 ANALYZING: {date}")
        print("=" * 50)
        
        anomalies = self.daily_anomalies[date]
        
        # Count different types of anomalies (excluding insufficient samples from anomaly count)
        plus_anomalies = [path for path, state in anomalies.items() if state == "+"]
        minus_anomalies = [path for path, state in anomalies.items() if state == "-"]
        insufficient_samples = [path for path, state in anomalies.items() if state == "S"]
        
        total_anomalies = len(plus_anomalies) + len(minus_anomalies)
        
        print(f"🚨 {total_anomalies} anomalies detected - performing analysis...")
        if insufficient_samples:
            print(f"⚠️  {len(insufficient_samples)} nodes excluded due to insufficient sample size (<5 responses)")
        
        # Generate tree interpretation (excluding insufficient samples from logic)
        tree_explanation = self._generate_tree_explanation(date, exclude_insufficient_sample=True)
        
        print("🌳 Tree with [Explanation needed] flags:")
        print("-" * 40)
        print(tree_explanation)
        
        return {
            "date": date,
            "total_anomalies": total_anomalies,
            "plus_anomalies": plus_anomalies,
            "minus_anomalies": minus_anomalies,
            "insufficient_samples": insufficient_samples,
            "tree_explanation": tree_explanation
        }

    def run_full_analysis(self, date_folder: str = "22_05_2025", min_sample_size: int = 5):
        """Run complete anomaly detection analysis"""
        print("🔍 STEP 2: Anomaly Detection")
        print("-" * 30)
        print(f"📊 Using data from: {date_folder}")
        
        # Load data
        self.load_data(date_folder)
        
        # Calculate moving averages (now mean of last 7 days)
        self.calculate_moving_averages()
        
        # Detect anomalies with minimum sample size filter
        self.detect_daily_anomalies(min_sample_size=min_sample_size)
        
        # Print summary
        self.print_all_days_summary()
        
        return self

    def _generate_tree_explanation(self, date: str, exclude_insufficient_sample: bool = True):
        """Generate tree explanation with hierarchical logic, optionally excluding insufficient samples"""
        if date not in self.daily_anomalies:
            return "No data available for this date"
            
        anomalies = self.daily_anomalies[date]
        explanation_lines = []
        
        # Helper function to get effective state (excluding insufficient samples if requested)
        def get_effective_state(path):
            state = anomalies.get(path, "?")
            if exclude_insufficient_sample and state == "S":
                return "?"  # Treat as no data for logic purposes
            return state
        
        # Helper function to get display state (always show actual state)
        def get_display_state(path):
            return anomalies.get(path, "?")
        
        # Helper function to check if node needs explanation
        def needs_explanation(path):
            state = get_effective_state(path)
            return state in ["+", "-"]
        
        explanation_lines.append(f"\n🌳 Anomaly Tree: {date}")
        explanation_lines.append("-" * 50)
        
        # Global level analysis
        global_state = get_effective_state("Global")
        global_display = get_display_state("Global")
        explanation_lines.append(f"Global [{global_display}]")
        
        if global_state == "N":
            # Analyze why Global is normal
            lh_state = get_effective_state("Global/LH")
            sh_state = get_effective_state("Global/SH")
            
            if lh_state == "N" and sh_state == "N":
                explanation_lines.append("  All children normal (LH, SH)")
            elif lh_state in ["+", "-"] and sh_state in ["+", "-"]:
                if lh_state != sh_state:
                    explanation_lines.append("  Anomalies in LH and SH cancel each other out")
                else:
                    explanation_lines.append("  Both LH and SH show anomalies but diluted at global level")
            elif lh_state in ["+", "-"]:
                explanation_lines.append(f"  {lh_state.replace('+', 'Positive').replace('-', 'Negative')} nodes (LH) diluted by normal nodes (SH)")
            elif sh_state in ["+", "-"]:
                explanation_lines.append(f"  {sh_state.replace('+', 'Positive').replace('-', 'Negative')} nodes (SH) diluted by normal nodes (LH)")
        
        # LH analysis
        lh_state = get_effective_state("Global/LH")
        lh_display = get_display_state("Global/LH")
        explanation_lines.append(f"  LH [{lh_display}]")
        
        if needs_explanation("Global/LH"):
            explanation_lines.append("    [Explanation needed]")
            
        if lh_state == "N":
            # Analyze LH children
            lh_children = ["Economy", "Business", "Premium"]
            lh_child_states = [get_effective_state(f"Global/LH/{child}") for child in lh_children]
            
            anomaly_children = [child for child, state in zip(lh_children, lh_child_states) if state in ["+", "-"]]
            normal_children = [child for child, state in zip(lh_children, lh_child_states) if state == "N"]
            
            if len(anomaly_children) == 0:
                explanation_lines.append(f"    All children normal ({', '.join(lh_children)})")
            elif len(anomaly_children) == 1:
                explanation_lines.append(f"    {anomaly_children[0]} anomaly diluted by normal nodes ({', '.join(normal_children)})")
            else:
                pos_children = [child for child, state in zip(lh_children, lh_child_states) if state == "+"]
                neg_children = [child for child, state in zip(lh_children, lh_child_states) if state == "-"]
                if pos_children and neg_children:
                    explanation_lines.append(f"    Mixed anomalies: positive ({', '.join(pos_children)}), negative ({', '.join(neg_children)}), normal ({', '.join(normal_children)}) balance out")
                else:
                    explanation_lines.append(f"    Multiple anomalies diluted by normal nodes")
        
        # LH children details
        for cabin in ["Economy", "Business", "Premium"]:
            cabin_path = f"Global/LH/{cabin}"
            cabin_state = get_effective_state(cabin_path)
            cabin_display = get_display_state(cabin_path)
            explanation_lines.append(f"    {cabin} [{cabin_display}]")
            if needs_explanation(cabin_path):
                explanation_lines.append("      [Explanation needed]")
        
        # SH analysis
        sh_state = get_effective_state("Global/SH")
        sh_display = get_display_state("Global/SH")
        explanation_lines.append(f"  SH [{sh_display}]")
        
        if needs_explanation("Global/SH"):
            explanation_lines.append("    [Explanation needed]")
            
        if sh_state == "N":
            # Analyze SH children
            economy_state = get_effective_state("Global/SH/Economy")
            business_state = get_effective_state("Global/SH/Business")
            
            if economy_state == "N" and business_state == "N":
                explanation_lines.append("    All children normal (Economy, Business)")
            elif economy_state in ["+", "-"] and business_state == "N":
                explanation_lines.append(f"    {economy_state.replace('+', 'Positive').replace('-', 'Negative')} nodes (Economy) diluted by normal nodes (Business)")
            elif business_state in ["+", "-"] and economy_state == "N":
                explanation_lines.append(f"    {business_state.replace('+', 'Positive').replace('-', 'Negative')} nodes (Business) diluted by normal nodes (Economy)")
            elif economy_state in ["+", "-"] and business_state in ["+", "-"]:
                if economy_state != business_state:
                    explanation_lines.append("    Economy and Business anomalies cancel each other out")
                else:
                    explanation_lines.append("    Both Economy and Business show anomalies but diluted at SH level")
        
        # SH Economy analysis
        economy_state = get_effective_state("Global/SH/Economy")
        economy_display = get_display_state("Global/SH/Economy")
        explanation_lines.append(f"    Economy [{economy_display}]")
        
        if needs_explanation("Global/SH/Economy"):
            explanation_lines.append("      [Explanation needed]")
            
        if economy_state == "N":
            # Analyze Economy children (IB, YW)
            ib_state = get_effective_state("Global/SH/Economy/IB")
            yw_state = get_effective_state("Global/SH/Economy/YW")
            
            if ib_state == "N" and yw_state == "N":
                explanation_lines.append("      All children normal (IB, YW)")
            elif ib_state in ["+", "-"] and yw_state == "N":
                explanation_lines.append(f"      {ib_state.replace('+', 'Positive').replace('-', 'Negative')} nodes (IB) diluted by normal nodes (YW)")
            elif yw_state in ["+", "-"] and ib_state == "N":
                explanation_lines.append(f"      {yw_state.replace('+', 'Positive').replace('-', 'Negative')} nodes (YW) diluted by normal nodes (IB)")
            elif ib_state in ["+", "-"] and yw_state in ["+", "-"]:
                if ib_state != yw_state:
                    explanation_lines.append("      IB and YW anomalies cancel each other out")
                else:
                    explanation_lines.append(f"      {ib_state.replace('+', 'Positive').replace('-', 'Negative')} anomaly consistent across all children (IB, YW)")
        
        # SH Economy children
        for company in ["IB", "YW"]:
            company_path = f"Global/SH/Economy/{company}"
            company_state = get_effective_state(company_path)
            company_display = get_display_state(company_path)
            explanation_lines.append(f"      {company} [{company_display}]")
            if needs_explanation(company_path):
                explanation_lines.append("        [Explanation needed]")
        
        # SH Business analysis
        business_state = get_effective_state("Global/SH/Business")
        business_display = get_display_state("Global/SH/Business")
        explanation_lines.append(f"    Business [{business_display}]")
        
        if needs_explanation("Global/SH/Business"):
            explanation_lines.append("      [Explanation needed]")
            
        if business_state == "N":
            # Analyze Business children (IB, YW)
            ib_state = get_effective_state("Global/SH/Business/IB")
            yw_state = get_effective_state("Global/SH/Business/YW")
            
            if ib_state == "N" and yw_state == "N":
                explanation_lines.append("      All children normal (IB, YW)")
            elif ib_state in ["+", "-"] and yw_state == "N":
                explanation_lines.append(f"      {ib_state.replace('+', 'Positive').replace('-', 'Negative')} nodes (IB) diluted by normal nodes (YW)")
            elif yw_state in ["+", "-"] and ib_state == "N":
                explanation_lines.append(f"      {yw_state.replace('+', 'Positive').replace('-', 'Negative')} nodes (YW) diluted by normal nodes (IB)")
            elif ib_state in ["+", "-"] and yw_state in ["+", "-"]:
                if ib_state != yw_state:
                    explanation_lines.append("      IB and YW anomalies cancel each other out")
                else:
                    explanation_lines.append(f"      {ib_state.replace('+', 'Positive').replace('-', 'Negative')} anomaly consistent across all children (IB, YW)")
        elif business_state in ["+", "-"]:
            # Check if it's consistent across children
            ib_state = get_effective_state("Global/SH/Business/IB")
            yw_state = get_effective_state("Global/SH/Business/YW")
            
            if ib_state == business_state and yw_state == business_state:
                explanation_lines.append(f"      {business_state.replace('+', 'Positive').replace('-', 'Negative')} anomaly consistent across all children (IB, YW)")
            elif ib_state == business_state and yw_state != business_state:
                explanation_lines.append(f"      {business_state.replace('+', 'Positive').replace('-', 'Negative')} nodes (IB) significant despite normal nodes (YW)")
            elif yw_state == business_state and ib_state != business_state:
                explanation_lines.append(f"      {business_state.replace('+', 'Positive').replace('-', 'Negative')} nodes (YW) significant despite normal nodes (IB)")
        
        # SH Business children
        for company in ["IB", "YW"]:
            company_path = f"Global/SH/Business/{company}"
            company_state = get_effective_state(company_path)
            company_display = get_display_state(company_path)
            explanation_lines.append(f"      {company} [{company_display}]")
            if needs_explanation(company_path):
                explanation_lines.append("        [Explanation needed]")
        
        return "\n".join(explanation_lines) 