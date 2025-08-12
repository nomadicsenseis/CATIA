import os
import boto3
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import tempfile
import logging
from io import StringIO
import re
from bs4 import BeautifulSoup

class NCSDataCollector:
    """Collects Net Customer Satisfaction data from AWS S3 bucket"""
    
    def __init__(self, temp_env_file: str = None):
        """
        Initialize NCS Data Collector
        
        Args:
            temp_env_file: Path to temporary credentials file
        """
        self.logger = logging.getLogger(__name__)
        
        # AWS S3 configuration
        self.bucket_name = "ibdata-prod-ew1-s3-customer"
        self.base_prefix = "customer/catia/ncs/raw/attatchments/"
        
        # Initialize AWS session
        self.s3_client = None
        self.temp_env_file = temp_env_file
        
        # Setup AWS credentials
        self._setup_aws_credentials()
        
    def _setup_aws_credentials(self):
        """Setup AWS credentials from temporary file or environment"""
        try:
            if self.temp_env_file and os.path.exists(self.temp_env_file):
                # Read credentials from temp file
                credentials = {}
                with open(self.temp_env_file, 'r') as f:
                    for line in f:
                        if '=' in line and not line.strip().startswith('#'):
                            key, value = line.strip().split('=', 1)
                            credentials[key.strip()] = value.strip()
                
                # Set up boto3 session with credentials
                session = boto3.Session(
                    aws_access_key_id=credentials.get('aws_access_key_id'),
                    aws_secret_access_key=credentials.get('aws_secret_access_key'),
                    aws_session_token=credentials.get('aws_session_token'),
                    region_name='eu-west-1'  # Based on bucket name
                )
                self.s3_client = session.client('s3')
                self.logger.info("✅ Successfully configured AWS credentials from temp file")
                
            else:
                # Fallback to environment variables
                self.s3_client = boto3.client('s3', region_name='eu-west-1')
                self.logger.info("✅ Using AWS credentials from environment")
                
        except Exception as e:
            self.logger.error(f"❌ Failed to setup AWS credentials: {str(e)}")
            raise
    
    def list_available_files(self, date_prefix: str = None) -> List[str]:
        """
        List available NCS files in S3 bucket
        
        Args:
            date_prefix: Optional date prefix to filter files (e.g., "2025-06")
            
        Returns:
            List of available file keys
        """
        try:
            prefix = self.base_prefix
            if date_prefix:
                prefix += f"ndc-{date_prefix}"
            
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix
            )
            
            files = []
            if 'Contents' in response:
                for obj in response['Contents']:
                    if obj['Key'].endswith('.txt'):
                        files.append(obj['Key'])
            
            self.logger.info(f"Found {len(files)} NCS files with prefix '{prefix}'")
            return files
            
        except Exception as e:
            self.logger.error(f"Error listing S3 files: {str(e)}")
            return []
    
    def read_ncs_file(self, file_key: str) -> pd.DataFrame:
        """
        Read a specific NCS file from S3 (HTML email format)
        
        Args:
            file_key: S3 key of the file to read
            
        Returns:
            DataFrame with NCS data extracted from HTML email
        """
        try:
            self.logger.info(f"Reading NCS file: s3://{self.bucket_name}/{file_key}")
            
            # Download file from S3
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=file_key)
            content = response['Body'].read().decode('utf-8')
            
            # Parse HTML email content
            df = self._parse_html_email_content(content, file_key)
            
            if not df.empty:
                self.logger.info(f"✅ Successfully parsed NCS email: {len(df)} rows, {len(df.columns)} columns")
            else:
                self.logger.warning(f"⚠️ No data extracted from NCS email")
            
            return df
            
        except Exception as e:
            self.logger.error(f"❌ Error reading NCS file {file_key}: {str(e)}")
            return pd.DataFrame()
    
    def _parse_html_email_content(self, content: str, file_key: str) -> pd.DataFrame:
        """
        Parse HTML email content to extract NCS incident data
        
        Args:
            content: Raw HTML email content
            file_key: File key for metadata
            
        Returns:
            DataFrame with parsed incident data
        """
        try:
            # Extract metadata from email headers
            email_metadata = self._extract_email_metadata(content)
            
            # Parse HTML content with BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')
            
            # Look for tables containing incident data
            tables = soup.find_all('table')
            
            all_data = []
            
            for table in tables:
                # Try to extract structured data from each table
                table_data = self._extract_table_data(table)
                if table_data:
                    all_data.extend(table_data)
            
            # If no tables found, try to extract data from text content
            if not all_data:
                all_data = self._extract_text_based_data(soup.get_text())
            
            if all_data:
                df = pd.DataFrame(all_data)
                
                # Add metadata columns
                df['source_file'] = file_key
                df['email_date'] = email_metadata.get('date')
                df['email_subject'] = email_metadata.get('subject')
                
                return df
            else:
                return pd.DataFrame()
                
        except Exception as e:
            self.logger.error(f"Error parsing HTML email content: {str(e)}")
            return pd.DataFrame()
    
    def _extract_email_metadata(self, content: str) -> Dict[str, str]:
        """Extract email metadata from HTML content"""
        metadata = {}
        
        try:
            # Extract subject
            subject_match = re.search(r'<b>Asunto:</b>\s*([^<]+)', content)
            if subject_match:
                metadata['subject'] = subject_match.group(1).strip()
            
            # Extract date
            date_match = re.search(r'<b>Enviados:</b>\s*([^<]+)', content)
            if date_match:
                metadata['date'] = date_match.group(1).strip()
            
            # Extract sender
            sender_match = re.search(r'<b>De:</b>\s*([^<]+)', content)
            if sender_match:
                metadata['sender'] = sender_match.group(1).strip()
                
        except Exception as e:
            self.logger.warning(f"Error extracting email metadata: {str(e)}")
            
        return metadata
    
    def _extract_table_data(self, table) -> List[Dict]:
        """Extract data from HTML table"""
        try:
            rows = table.find_all('tr')
            if not rows:
                return []
            
            # Try to identify header row
            headers = []
            data_rows = []
            
            for i, row in enumerate(rows):
                cells = row.find_all(['th', 'td'])
                if not cells:
                    continue
                
                cell_texts = [cell.get_text(strip=True) for cell in cells]
                
                # If first row or contains header-like text, treat as headers
                if i == 0 or any('incident' in cell.lower() or 'flight' in cell.lower() or 'route' in cell.lower() for cell in cell_texts):
                    if not headers:  # Only set headers once
                        headers = cell_texts
                else:
                    data_rows.append(cell_texts)
            
            # Convert to list of dictionaries
            if headers and data_rows:
                result = []
                for row in data_rows:
                    # Pad row to match headers length
                    while len(row) < len(headers):
                        row.append('')
                    
                    row_dict = {}
                    for j, header in enumerate(headers):
                        if j < len(row):
                            row_dict[header] = row[j]
                    
                    # Only add non-empty rows
                    if any(value.strip() for value in row_dict.values()):
                        result.append(row_dict)
                
                return result
            
        except Exception as e:
            self.logger.warning(f"Error extracting table data: {str(e)}")
            
        return []
    
    def _extract_text_based_data(self, text_content: str) -> List[Dict]:
        """Extract incident data from plain text content using patterns"""
        try:
            incidents = []
            
            # Look for common incident patterns
            # This is a flexible approach to extract key information
            
            # Split text into lines and look for incident-like patterns
            lines = text_content.split('\n')
            
            current_incident = {}
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Look for flight numbers (IB followed by digits)
                flight_match = re.search(r'(IB\d+)', line, re.IGNORECASE)
                if flight_match:
                    if current_incident:
                        incidents.append(current_incident)
                    current_incident = {'flight': flight_match.group(1)}
                
                # Look for routes (XXX-YYY pattern)
                route_match = re.search(r'([A-Z]{3})-([A-Z]{3})', line)
                if route_match and current_incident:
                    current_incident['route'] = f"{route_match.group(1)}-{route_match.group(2)}"
                
                # Look for times (HH:MM format)
                time_match = re.search(r'(\d{1,2}:\d{2})', line)
                if time_match and current_incident:
                    if 'time' not in current_incident:
                        current_incident['time'] = time_match.group(1)
                
                # Look for incident descriptions (lines containing certain keywords)
                incident_keywords = ['delay', 'cancel', 'incident', 'problem', 'issue', 'technical']
                if any(keyword in line.lower() for keyword in incident_keywords):
                    if current_incident:
                        current_incident['description'] = line
            
            # Add the last incident if any
            if current_incident:
                incidents.append(current_incident)
            
            return incidents
            
        except Exception as e:
            self.logger.warning(f"Error extracting text-based data: {str(e)}")
            return []
    
    def read_ncs_file_by_path(self, s3_path: str) -> pd.DataFrame:
        """
        Read NCS file by full S3 path (HTML email format)
        
        Args:
            s3_path: Full S3 path (e.g., "s3://bucket/path/file.txt")
            
        Returns:
            DataFrame with NCS data extracted from HTML email
        """
        try:
            # Extract bucket and key from S3 path
            if not s3_path.startswith('s3://'):
                raise ValueError("S3 path must start with 's3://'")
            
            path_parts = s3_path[5:].split('/', 1)  # Remove 's3://' and split
            bucket = path_parts[0]
            key = path_parts[1] if len(path_parts) > 1 else ""
            
            self.logger.info(f"Reading NCS file from: {s3_path}")
            
            # Download file from S3
            response = self.s3_client.get_object(Bucket=bucket, Key=key)
            content = response['Body'].read().decode('utf-8')
            
            # Parse HTML email content
            df = self._parse_html_email_content(content, key)
            
            if not df.empty:
                self.logger.info(f"✅ Successfully parsed NCS email: {len(df)} rows, {len(df.columns)} columns")
            else:
                self.logger.warning(f"⚠️ No data extracted from NCS email")
            
            return df
            
        except Exception as e:
            self.logger.error(f"❌ Error reading NCS file from {s3_path}: {str(e)}")
            return pd.DataFrame()
    
    def collect_ncs_data_for_date_range(self, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """
        Collect NCS data for a specific date range
        
        Args:
            start_date: Start date for data collection
            end_date: End date for data collection
            
        Returns:
            Combined DataFrame with NCS data for the date range
        """
        try:
            self.logger.info(f"Collecting NCS data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
            print(f"🔍 DEBUG NCSDataCollector: Collecting data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
            
            all_data = []
            current_date = start_date
            total_files_found = 0
            total_files_processed = 0
            
            while current_date <= end_date:
                date_str = current_date.strftime('%Y-%m-%d')
                print(f"🔍 DEBUG NCSDataCollector: Processing date {date_str}")
                files = self.list_available_files(date_str)
                total_files_found += len(files)
                print(f"🔍 DEBUG NCSDataCollector: Found {len(files)} files for {date_str}: {files[:3] if files else 'None'}")
                
                for file_key in files:
                    print(f"🔍 DEBUG NCSDataCollector: Reading file {file_key}")
                    df = self.read_ncs_file(file_key)
                    if not df.empty:
                        print(f"✅ DEBUG NCSDataCollector: File {file_key} loaded with {len(df)} rows")
                        # Add metadata
                        df['source_file'] = file_key
                        df['collection_date'] = current_date
                        all_data.append(df)
                        total_files_processed += 1
                    else:
                        print(f"⚠️ DEBUG NCSDataCollector: File {file_key} is EMPTY or failed to load")
                
                current_date += timedelta(days=1)
            
            if all_data:
                combined_df = pd.concat(all_data, ignore_index=True)
                self.logger.info(f"✅ Collected {len(combined_df)} total NCS records")
                print(f"✅ DEBUG NCSDataCollector: Final result: {len(combined_df)} total records from {len(all_data)} files")
                print(f"✅ DEBUG NCSDataCollector: Date range processed: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
                print(f"✅ DEBUG NCSDataCollector: Files summary: {total_files_found} found, {total_files_processed} processed successfully")
                return combined_df
            else:
                self.logger.warning("No NCS data found for the specified date range")
                print(f"⚠️ DEBUG NCSDataCollector: NO DATA FOUND for range {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
                print(f"⚠️ DEBUG NCSDataCollector: Total dates checked: {(end_date - start_date).days + 1}")
                return pd.DataFrame()
                
        except Exception as e:
            self.logger.error(f"❌ Error collecting NCS data: {str(e)}")
            return pd.DataFrame()
    
    def collect_ncs_data_for_period(self, analysis_date: datetime, target_period: int, aggregation_days: int) -> pd.DataFrame:
        """
        Collect NCS data for a specific period in the flexible aggregation system
        
        Args:
            analysis_date: The reference date for the analysis
            target_period: Period number (1 = most recent relative to analysis_date)
            aggregation_days: Days per period (1, 7, 14, 30, etc.)
            
        Returns:
            Combined DataFrame with NCS data for the period
            
        Examples:
            For daily analysis (aggregation_days=1):
            - Period 1: NCS data for analysis_date only
            - Period 2: NCS data for analysis_date - 1 day
            
            For weekly analysis (aggregation_days=7):
            - Period 1: NCS data for the 7 days ending on analysis_date
            - Period 2: NCS data for the 7 days before that
        """
        try:
            # Calculate the date range for this period
            start_date, end_date = self._calculate_period_date_range(analysis_date, target_period, aggregation_days)
            
            self.logger.info(f"Collecting NCS data for Period {target_period} ({aggregation_days}d aggregation)")
            self.logger.info(f"Date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
            
            # Collect data for the date range
            df = self.collect_ncs_data_for_date_range(start_date, end_date)
            
            if not df.empty:
                # Add period metadata
                df['period_number'] = target_period
                df['aggregation_days'] = aggregation_days
                df['period_start_date'] = start_date
                df['period_end_date'] = end_date
                
                self.logger.info(f"✅ Collected {len(df)} NCS records for Period {target_period}")
            
            return df
            
        except Exception as e:
            self.logger.error(f"❌ Error collecting NCS data for period: {str(e)}")
            return pd.DataFrame()
    
    def collect_ncs_data_for_multiple_periods(self, analysis_date: datetime, periods: List[int], aggregation_days: int) -> Dict[int, pd.DataFrame]:
        """
        Collect NCS data for multiple periods
        
        Args:
            analysis_date: The reference date for the analysis
            periods: List of period numbers to collect
            aggregation_days: Days per period
            
        Returns:
            Dictionary mapping period number to DataFrame with NCS data
        """
        results = {}
        
        for period in periods:
            try:
                df = self.collect_ncs_data_for_period(analysis_date, period, aggregation_days)
                if not df.empty:
                    results[period] = df
                    self.logger.info(f"✅ Period {period}: {len(df)} incidents")
                else:
                    self.logger.warning(f"⚠️ Period {period}: No data found")
            except Exception as e:
                self.logger.error(f"❌ Period {period}: {str(e)}")
        
        total_incidents = sum(len(df) for df in results.values())
        self.logger.info(f"📊 Collected NCS data for {len(results)}/{len(periods)} periods ({total_incidents} total incidents)")
        
        return results
    
    def _calculate_period_date_range(self, analysis_date: datetime, target_period: int, aggregation_days: int) -> tuple:
        """
        Calculate the correct date range for a period relative to the analysis date
        (Same logic as in main.py calculate_period_date_range)
        
        Args:
            analysis_date: The reference date for the analysis
            target_period: Period number (1 = most recent relative to analysis_date)
            aggregation_days: Days per period (1, 7, 14, 30, etc.)
            
        Returns:
            Tuple of (start_date, end_date) for the target period
        """
        # Calculate how many days back from analysis date
        days_back = (target_period - 1) * aggregation_days
        
        # For daily analysis, each period is exactly one day
        # For weekly analysis, each period is 7 days, etc.
        period_end = analysis_date - timedelta(days=days_back)
        period_start = period_end - timedelta(days=aggregation_days - 1)
        
        return period_start, period_end
    
    def get_latest_ncs_file(self) -> Optional[str]:
        """
        Get the most recent NCS file
        
        Returns:
            Key of the latest NCS file or None if no files found
        """
        try:
            files = self.list_available_files()
            if not files:
                return None
            
            # Sort files by name (assuming timestamp in filename)
            files.sort(reverse=True)
            latest_file = files[0]
            
            self.logger.info(f"Latest NCS file: {latest_file}")
            return latest_file
            
        except Exception as e:
            self.logger.error(f"Error finding latest NCS file: {str(e)}")
            return None
    
    def save_ncs_data(self, df: pd.DataFrame, output_path: str) -> bool:
        """
        Save NCS data to local file
        
        Args:
            df: DataFrame to save
            output_path: Local path to save the file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            if output_path.endswith('.csv'):
                df.to_csv(output_path, index=False)
            elif output_path.endswith('.parquet'):
                df.to_parquet(output_path, index=False)
            else:
                # Default to CSV
                df.to_csv(output_path, index=False)
            
            self.logger.info(f"✅ Saved NCS data to {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error saving NCS data: {str(e)}")
            return False
    
    def analyze_ncs_incidents_for_period(self, df: pd.DataFrame, analysis_focus: str = "all") -> Dict[str, Any]:
        """
        Analyze NCS incidents to provide operational insights
        Enhanced to match causal agent expectations
        
        Args:
            df: DataFrame with NCS incident data
            analysis_focus: Focus of analysis ("flights", "routes", "incidents", "all")
            
        Returns:
            Dictionary with analysis results including incident_counts structure expected by causal agent
        """
        if df.empty:
            return {
                "total_incidents": 0, 
                "analysis": "No incidents found",
                "incident_counts": {},
                "detailed_incidents": {"count": 0, "sample_incidents": []},
                "route_analysis": {},
                "flight_analysis": {}
            }
        
        analysis = {
            "total_incidents": len(df),
            "date_range": {
                "start": df['period_start_date'].iloc[0] if 'period_start_date' in df.columns else None,
                "end": df['period_end_date'].iloc[0] if 'period_end_date' in df.columns else None
            },
            "period_info": {
                "period_number": df['period_number'].iloc[0] if 'period_number' in df.columns else None,
                "aggregation_days": df['aggregation_days'].iloc[0] if 'aggregation_days' in df.columns else None
            }
        }
        
        try:
            # ENHANCED: Generate incident_counts structure expected by causal agent
            incident_counts = self._extract_incident_counts_from_data(df)
            analysis["incident_counts"] = incident_counts
            
            # Analyze flight impacts
            if analysis_focus in ["flights", "all"] and not df.empty:
                flight_incidents = df[df.iloc[:, 0].str.contains('IB\\d+', na=False, regex=True)]
                if not flight_incidents.empty:
                    flight_counts = flight_incidents.iloc[:, 0].value_counts()
                    analysis["flight_analysis"] = {
                        "total_flights_affected": len(flight_counts),
                        "most_affected_flights": flight_counts.head(5).to_dict(),
                        "flight_impact_summary": f"{len(flight_counts)} flights affected with {len(flight_incidents)} total flight-related incidents"
                    }
                else:
                    analysis["flight_analysis"] = {
                        "total_flights_affected": 0,
                        "most_affected_flights": {},
                        "flight_impact_summary": "No flight-specific incidents found"
                    }
            
            # Analyze incident categories
            if analysis_focus in ["incidents", "all"]:
                # Look for incident type patterns in the data
                incident_categories = []
                
                # Check column names for incident types
                for col in df.columns:
                    if any(keyword in col.lower() for keyword in ['cancel', 'retraso', 'incident', 'equipaje', 'tecnic', 'desvio']):
                        if col not in ['source_file', 'email_date', 'email_subject']:
                            incident_categories.append(col)
                
                if incident_categories:
                    analysis["incident_categories"] = {
                        "categories_found": incident_categories,
                        "category_summary": f"Found {len(incident_categories)} incident categories in the data"
                    }
                
                # Analyze incident descriptions - ENHANCED for causal agent
                detailed_incidents = df[df.iloc[:, 0].str.len() > 50]
                if not detailed_incidents.empty:
                    # Extract key incident themes
                    incident_texts = detailed_incidents.iloc[:, 0].tolist()
                    analysis["detailed_incidents"] = {
                        "count": len(detailed_incidents),
                        "sample_incidents": incident_texts[:3],  # First 3 as examples
                        "incident_themes": self._extract_incident_themes(incident_texts)
                    }
                else:
                    analysis["detailed_incidents"] = {
                        "count": 0,
                        "sample_incidents": [],
                        "incident_themes": []
                    }
            
            # Analyze routes (if available) - ENHANCED
            if analysis_focus in ["routes", "all"]:
                route_analysis = self._extract_route_analysis_from_data(df)
                analysis["route_analysis"] = route_analysis
            
            # Generate summary insights
            analysis["summary_insights"] = self._generate_summary_insights(analysis)
            
        except Exception as e:
            analysis["error"] = f"Error during analysis: {str(e)}"
        
        return analysis
    
    def _extract_incident_themes(self, incident_texts: List[str]) -> List[str]:
        """Extract common themes from incident descriptions"""
        themes = []
        
        # Define incident theme keywords
        theme_keywords = {
            "technical_issues": ["técnica", "technical", "avería", "breakdown", "maintenance"],
            "weather": ["weather", "tiempo", "meteorológica", "tormenta", "storm"],
            "bird_strike": ["aves", "bird", "impacto", "strike"],
            "delays": ["retraso", "delay", "delayed", "tardanza"],
            "cancellations": ["cancel", "anulado", "cancelled"],
            "aircraft_change": ["cambio", "change", "aircraft", "avión"],
            "baggage": ["equipaje", "baggage", "maleta", "luggage"],
            "crew": ["tripulación", "crew", "piloto", "pilot"],
            "passenger": ["pasajero", "passenger", "cliente", "customer"]
        }
        
        theme_counts = {}
        
        for theme, keywords in theme_keywords.items():
            count = 0
            for text in incident_texts:
                if any(keyword.lower() in text.lower() for keyword in keywords):
                    count += 1
            if count > 0:
                theme_counts[theme] = count
        
        # Return themes sorted by frequency
        for theme, count in sorted(theme_counts.items(), key=lambda x: x[1], reverse=True):
            themes.append(f"{theme}: {count} incidents")
        
        return themes[:5]  # Top 5 themes
    
    def _generate_summary_insights(self, analysis: Dict) -> List[str]:
        """Generate human-readable insights from analysis"""
        insights = []
        
        total = analysis.get("total_incidents", 0)
        insights.append(f"Total of {total} operational incidents detected")
        
        if "flight_analysis" in analysis:
            flight_info = analysis["flight_analysis"]
            insights.append(f"Flight impact: {flight_info['total_flights_affected']} flights affected")
            
            if flight_info.get("most_affected_flights"):
                top_flight = list(flight_info["most_affected_flights"].items())[0]
                insights.append(f"Most affected flight: {top_flight[0]} ({top_flight[1]} incidents)")
        
        if "incident_categories" in analysis:
            cat_count = len(analysis["incident_categories"]["categories_found"])
            insights.append(f"Incident diversity: {cat_count} different categories identified")
        
        if "detailed_incidents" in analysis:
            detail_count = analysis["detailed_incidents"]["count"]
            insights.append(f"Detailed incidents: {detail_count} complex operational issues")
        
        if "route_analysis" in analysis:
            route_count = analysis["route_analysis"]["total_routes_affected"]
            insights.append(f"Route impact: {route_count} routes experienced incidents")
        
        return insights 
    
    def _extract_incident_counts_from_data(self, df: pd.DataFrame) -> Dict[str, int]:
        """
        Extract incident counts by type from NCS data
        Returns structure expected by causal agent: {incident_type: count}
        """
        incident_counts = {}
        
        # Map from column names to standard incident types expected by causal agent
        incident_type_mapping = {
            'cancelaciones': ['Cancelaciones', 'Cancel'],
            'retrasos': ['Retrasos', 'Delay'],
            'desvios': ['Desvíos', 'Divert'],
            'limitacion_aeronave': ['Limitación', 'Aircraft'],
            'equipaje': ['Equipaje', 'Baggage'],
            'otras_incidencias': ['Otras incidencias', 'Other', 'Otros'],
            'incidencias_sistemas': ['Incidencias con sistemas', 'System']
        }
        
        # Extract counts from column data
        for standard_type, column_variants in incident_type_mapping.items():
            count = 0
            for variant in column_variants:
                # Check for exact column match
                matching_cols = [col for col in df.columns if variant.lower() in col.lower()]
                for col in matching_cols:
                    if col in df.columns:
                        # Sum non-empty values in this column
                        col_data = df[col].dropna()
                        if len(col_data) > 0:
                            # Count non-empty, non-zero entries
                            non_empty = col_data[col_data.astype(str).str.strip() != '']
                            if len(non_empty) > 0:
                                try:
                                    # Try to sum numeric values
                                    numeric_data = pd.to_numeric(non_empty, errors='ignore')
                                    if numeric_data.dtype in ['int64', 'float64']:
                                        count += int(numeric_data.sum())
                                    else:
                                        count += len(non_empty)
                                except:
                                    count += len(non_empty)
            
            if count > 0:
                incident_counts[standard_type] = count
        
        # If no specific columns found, analyze the main incident text column
        if not incident_counts and not df.empty:
            main_col = df.columns[0]
            all_text = " ".join(df[main_col].astype(str).tolist()).lower()
            
            # Simple text-based counting as fallback
            text_mapping = {
                'cancelaciones': ['cancel', 'anulad', 'cancelled'],
                'retrasos': ['retraso', 'delay', 'delayed', 'tarde'],
                'desvios': ['desvio', 'divert', 'reroute'],
                'limitacion_aeronave': ['aircraft', 'avión', 'aeronave', 'technical'],
                'equipaje': ['equipaje', 'baggage', 'maleta', 'luggage'],
                'otras_incidencias': ['other', 'otro', 'misc', 'various']
            }
            
            for incident_type, keywords in text_mapping.items():
                count = sum(all_text.count(keyword) for keyword in keywords)
                if count > 0:
                    incident_counts[incident_type] = count
        
        return incident_counts
    
    def _extract_route_analysis_from_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Extract route analysis optimized for causal agent expectations
        """
        if df.empty:
            return {
                "total_routes_affected": 0,
                "most_affected_routes": {},
                "route_impact_summary": "No route data available"
            }
        
        route_pattern = r'[A-Z]{3}-[A-Z]{3}'
        routes = []
        
        # Extract routes from all text columns
        for col in df.columns:
            if col not in ['source_file', 'email_date', 'email_subject', 'collection_date']:
                route_incidents = df[df[col].astype(str).str.contains(route_pattern, na=False, regex=True)]
                for text in route_incidents[col]:
                    route_matches = re.findall(route_pattern, str(text))
                    routes.extend(route_matches)
        
        if routes:
            route_counts = pd.Series(routes).value_counts()
            return {
                "total_routes_affected": len(route_counts),
                "most_affected_routes": route_counts.head(5).to_dict(),
                "route_impact_summary": f"{len(route_counts)} routes affected with {len(routes)} total route-related incidents",
                "all_routes": list(set(routes))
            }
        else:
            return {
                "total_routes_affected": 0,
                "most_affected_routes": {},
                "route_impact_summary": "No routes identified in incidents",
                "all_routes": []
            }
    
    def create_temporal_comparison_analysis(self, current_data: pd.DataFrame, comparison_data: pd.DataFrame, 
                                          current_period: str, comparison_period: str, node_path: str = None) -> Dict[str, Any]:
        """
        Create temporal comparison analysis between two periods for causal agent
        Returns structure expected by _create_temporal_ncs_comparison
        """
        try:
            # Extract structured data for both periods
            current_structured = self._extract_structured_data_for_comparison(current_data, "current")
            comparison_structured = self._extract_structured_data_for_comparison(comparison_data, "comparison")
            
            # Create route × incident type matrix
            route_incident_matrix = self._create_route_incident_matrix(current_structured, comparison_structured)
            
            # Calculate global deltas by incident type
            incident_type_deltas = self._calculate_incident_type_deltas(current_structured, comparison_structured)
            
            # Identify patterns and trends
            improvement_patterns = self._identify_improvement_patterns(route_incident_matrix, incident_type_deltas)
            
            # Create comprehensive analysis
            temporal_analysis = {
                'current_period': current_period,
                'comparison_period': comparison_period,
                'route_incident_matrix': route_incident_matrix,
                'incident_type_deltas': incident_type_deltas,
                'improvement_patterns': improvement_patterns,
                'current_structured': current_structured,
                'comparison_structured': comparison_structured,
                'analysis_summary': self._generate_temporal_summary(route_incident_matrix, incident_type_deltas, improvement_patterns)
            }
            
            return temporal_analysis
            
        except Exception as e:
            self.logger.error(f"Error creating temporal NCS comparison: {str(e)}")
            return {
                'error': str(e),
                'current_period': current_period,
                'comparison_period': comparison_period,
                'analysis_summary': f"❌ Error in temporal comparison: {str(e)}"
            }
    
    def _extract_structured_data_for_comparison(self, data: pd.DataFrame, period_label: str) -> Dict[str, Any]:
        """Extract structured NCS data optimized for temporal comparison"""
        if data.empty:
            return {
                'period': period_label,
                'total_incidents': 0,
                'route_incidents': {},
                'incident_types': {
                    'cancelaciones': 0,
                    'retrasos': 0,
                    'desvios': 0,
                    'limitacion_aeronave': 0,
                    'otras_incidencias': 0
                },
                'routes': []
            }
        
        # Get incident counts using existing method
        incident_counts = self._extract_incident_counts_from_data(data)
        
        # Get route analysis
        route_analysis = self._extract_route_analysis_from_data(data)
        
        # Build structured data
        structured_data = {
            'period': period_label,
            'total_incidents': len(data),
            'route_incidents': {},  # Could be enhanced with route-specific incident mapping
            'incident_types': {
                'cancelaciones': incident_counts.get('cancelaciones', 0),
                'retrasos': incident_counts.get('retrasos', 0),
                'desvios': incident_counts.get('desvios', 0),
                'limitacion_aeronave': incident_counts.get('limitacion_aeronave', 0),
                'otras_incidencias': incident_counts.get('otras_incidencias', 0)
            },
            'routes': route_analysis.get('all_routes', [])
        }
        
        return structured_data
    
    def _create_route_incident_matrix(self, current_structured: Dict, comparison_structured: Dict) -> Dict[str, Dict]:
        """Create route × incident type matrix with deltas"""
        matrix = {}
        
        # Get all unique routes from both periods
        current_routes = set(current_structured.get('routes', []))
        comparison_routes = set(comparison_structured.get('routes', []))
        all_routes = current_routes.union(comparison_routes)
        
        # For now, create a simplified matrix
        # This could be enhanced with more sophisticated route-incident mapping
        for route in all_routes:
            matrix[route] = {
                'current_incidents': 1 if route in current_routes else 0,
                'comparison_incidents': 1 if route in comparison_routes else 0,
                'delta': (1 if route in current_routes else 0) - (1 if route in comparison_routes else 0)
            }
        
        return matrix
    
    def _calculate_incident_type_deltas(self, current_structured: Dict, comparison_structured: Dict) -> Dict[str, Dict]:
        """Calculate deltas by incident type between periods"""
        deltas = {}
        
        current_types = current_structured.get('incident_types', {})
        comparison_types = comparison_structured.get('incident_types', {})
        
        # Get all incident types
        all_types = set(current_types.keys()).union(set(comparison_types.keys()))
        
        for incident_type in all_types:
            current_count = current_types.get(incident_type, 0)
            comparison_count = comparison_types.get(incident_type, 0)
            delta = current_count - comparison_count
            
            deltas[incident_type] = {
                'current': current_count,
                'comparison': comparison_count,
                'delta': delta,
                'change_pct': round((delta / comparison_count * 100), 1) if comparison_count > 0 else 0
            }
        
        return deltas
    
    def _identify_improvement_patterns(self, route_matrix: Dict, incident_deltas: Dict) -> Dict[str, Any]:
        """Identify improvement or deterioration patterns"""
        patterns = {
            'improving_incident_types': [],
            'worsening_incident_types': [],
            'new_affected_routes': [],
            'recovered_routes': []
        }
        
        # Analyze incident type trends
        for incident_type, delta_data in incident_deltas.items():
            if delta_data['delta'] < 0:  # Improvement (fewer incidents)
                patterns['improving_incident_types'].append({
                    'type': incident_type,
                    'improvement': abs(delta_data['delta']),
                    'change_pct': delta_data['change_pct']
                })
            elif delta_data['delta'] > 0:  # Worsening (more incidents)
                patterns['worsening_incident_types'].append({
                    'type': incident_type,
                    'increase': delta_data['delta'],
                    'change_pct': delta_data['change_pct']
                })
        
        # Analyze route trends
        for route, route_data in route_matrix.items():
            if route_data['delta'] > 0:  # New affected route
                patterns['new_affected_routes'].append(route)
            elif route_data['delta'] < 0:  # Route recovered
                patterns['recovered_routes'].append(route)
        
        return patterns
    
    def _generate_temporal_summary(self, route_matrix: Dict, incident_deltas: Dict, patterns: Dict) -> str:
        """Generate summary for temporal comparison"""
        summary_parts = []
        
        # Overall trend
        total_current = sum(delta['current'] for delta in incident_deltas.values())
        total_comparison = sum(delta['comparison'] for delta in incident_deltas.values())
        overall_delta = total_current - total_comparison
        
        if overall_delta > 0:
            summary_parts.append(f"📈 Overall increase: +{overall_delta} total incidents")
        elif overall_delta < 0:
            summary_parts.append(f"📉 Overall improvement: {overall_delta} total incidents")
        else:
            summary_parts.append("📊 Stable incident levels between periods")
        
        # Key changes
        if patterns['worsening_incident_types']:
            worst = max(patterns['worsening_incident_types'], key=lambda x: x['increase'])
            summary_parts.append(f"🔴 Most increased: {worst['type']} (+{worst['increase']})")
        
        if patterns['improving_incident_types']:
            best = max(patterns['improving_incident_types'], key=lambda x: x['improvement'])
            summary_parts.append(f"🟢 Most improved: {best['type']} (-{best['improvement']})")
        
        return " | ".join(summary_parts) if summary_parts else "No significant changes detected" 