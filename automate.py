import subprocess
import sys
import time

def run_script(script_name):
    """Executes a python script and handles errors."""
    print(f"\n{'='*50}")
    print(f"🚀 RUNNING: {script_name}")
    print(f"{'='*50}\n")
    
    try:
        # sys.executable ensures it uses your current Python environment
        subprocess.run([sys.executable, script_name], check=True)
        print(f"\n✅ SUCCESS: {script_name} completed.")
        time.sleep(1) # Tiny pause for readability in the terminal
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ ERROR: {script_name} crashed!")
        print("Halting the pipeline to prevent cascading errors.")
        sys.exit(1) # Stop the master script if a sub-script fails

def execute_pipeline():
    """Chains the entire analytical workflow into a single command."""
    print("Starting the Automated Sales Analysis Pipeline...\n")
    start_time = time.time()
    
    # ---------------------------------------------------------
    # THE PIPELINE ORDER
    # ---------------------------------------------------------
    # Note: Add 'setup_sql.py' and 'analysis.py' back into this 
    # list once you have them updated for the new dataset!
    # ---------------------------------------------------------
    
        # ---------------------------------------------------------
    # THE PIPELINE ORDER
    # ---------------------------------------------------------
    import os
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    scripts_to_run = [
        os.path.join(BASE_DIR, "scripts", "cleaning.py"),
        os.path.join(BASE_DIR, "scripts", "segmentation.py")
    ]
    
    
    for script in scripts_to_run:
        run_script(script)
        
    end_time = time.time()
    total_time = round(end_time - start_time, 2)
    
    print(f"\n{'='*50}")
    print(f"🎉 PIPELINE COMPLETE IN {total_time} SECONDS!")
    print(f"{'='*50}\n")

if __name__ == "__main__":
    execute_pipeline()