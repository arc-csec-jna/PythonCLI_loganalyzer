
from pathlib import Path
import argparse
from collections import Counter
import json
from datetime import datetime, timezone

def parse_args():
     parser = argparse.ArgumentParser(description="Simple Log Analyzer")
     parser.add_argument('-t','--top', type=int,default=3,help='display top # of log entries')
     parser.add_argument('-f','--file', type=str,required=True,help='Enter the log filename here')
     parser.add_argument('-o','--output', type=str,default='summary.txt',help='Output log file result')
     parser.add_argument('-j','--json_dir',default="JSONsummary",help='JSON directory to save report')
     return parser.parse_args()


def parse_Error_line(line):
     P_lineResult = line.strip().split(" ",3)
     if len(P_lineResult) >= 3:
          Error_level = P_lineResult[2] 
          return(Error_level)
     else:
          return "UNKNOWN"

def parse_message_line(line): 
     P_lineResult = line.strip().split(" ",4)
     if len(P_lineResult) >= 4:
          message = P_lineResult[4]
          message = message.strip().lower()
          return message

def parse_timestamp(line): 
     P_lineResult = line.strip().split(" ",3)
     if len(P_lineResult) >= 3:
          timestamp =  P_lineResult[0] +" "+ P_lineResult[1]
          return timestamp

def count_levels(log_path):
     Counters = {"INFO":0,"WARN":0,"ERROR":0,"UNKNOWN":0}
     error_counter = Counter()
     first_error_timestamp = None
     last_error_timestamp = None
     try:
          with log_path.open() as file:
               for line in file:
                    parts = parse_Error_line(line)
                    error_message =  parse_message_line(line)
                    parse_time = parse_timestamp(line)

                    if parts in Counters:
                         Counters[parts] +=1
                    else:
                         Counters["UNKNOWN"] +=1

                    if parts == "ERROR":
                         error_counter[error_message] +=1
                         if first_error_timestamp == None:
                              first_error_timestamp = parse_time.strip()
                         last_error_timestamp = parse_time.strip()
                         
     except FileNotFoundError:
          print("Log file not found:",log_path)
     return Counters, error_counter,first_error_timestamp,last_error_timestamp

def save_report(output_file,counts,error_counter,top_n,first_error,last_error):
     with open(output_file,"w",encoding="utf-8") as f:
          f.write("Log Summary \n")
          f.write("-------------------------\n")
          f.write(f"INFO:{counts.get('INFO',0)}\n")
          f.write(f"WARN:{counts.get('WARN',0)}\n")
          f.write(f"ERROR:{counts.get('ERROR',0)}\n\n")
          f.write(f"\nFirst Error Time: {first_error}\n")
          f.write(f"Last Error Time: {last_error}\n")
          f.write(f"Top {top_n} Errors:\n\n")

          for msg,count in error_counter.most_common(top_n):
               f.write(f"{count} x {msg}\n")

def export_json_report(out_path:str, log_dir:str,level_counts:dict,error_cnts:dict,first_err:str| None, last_err:str | None, top_errors:int):
     
     sorted_errors = sorted(error_cnts.items(),key=lambda kv:kv[1], reverse=True)

     report = {
          "meta": {
               "log_file": str(log_dir),
               "generated_at": datetime.now(timezone.utc).isoformat(),
               "top_n": top_errors,
          },
          "counts": level_counts,
          "first_error": first_err,
          "last_error": last_err,
          "top_errors": sorted_errors[:top_errors],
          "error_groupings": sorted_errors
     }
     
     with open(out_path,"w", encoding="utf-8") as f:
          json.dump(report,f,indent=2)

def main():
     args = parse_args()
     file_path = Path(args.file)
     counts, error_counter,first_error,last_error =  count_levels(file_path)

     print("\n Log Summary")
     print("------------------------")
     print(f"INFO:{counts.get('INFO',0)}")
     print(f"WARN:{counts.get('WARN',0)}")
     print(f"ERROR:{counts.get('ERROR',0)}")
     print(f"Top {args.top}")
     print(f"\nTop {args.top} Errors:")
     print(f"\nFirst Error Time: {first_error}")
     print(f"Last Error Time: {last_error}\n")
     for msg, count in error_counter.most_common(args.top):
          print(f"{count} x {msg}")
          save_report(args.output, counts, error_counter, args.top,first_error,last_error)
     print(f"\nReport saved to {args.output}")

     print("exporting JSON files")
     print("------------------------")
     
     if args.json_dir:
          json_dir = Path(args.json_dir)
          json_dir.mkdir(parents=True, exist_ok=True)

          log_name = Path(args.output).stem
          json_file_path = json_dir / f"{log_name}_report.json"

     export_json_report(json_file_path,file_path,counts,error_counter,first_error,last_error,args.top)

if __name__ == "__main__":
     '''      
          base_dir = Path(__file__).resolve().parent.parent
          fileFormat = "syslog"
          logPath = base_dir/"src"/"data"/"sample"/"system.log"
          counts = count_levels(logPath)     
          print(counts.get("INFO"))
     '''
main()
