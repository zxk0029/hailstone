#!/bin/bash

# --- Check if running from project root ---
if [ ! -f ".gitmodules" ]; then
    echo "Error: This script must be run from the project root directory (the directory containing .gitmodules)." >&2
    echo "Usage: cd /path/to/project/root && bash scripts/proto_compile.sh" >&2
    exit 1
fi

# --- Define Key Paths (Relative to project root) ---
PROTO_SUBMODULE_DIR="external/dapplink-proto"
PROTO_SRC_DIR="$PROTO_SUBMODULE_DIR/dapplink" # Source protos within the submodule
PYTHON_INTERMEDIATE_DIR="python_build_temp" # Intermediate build directory relative to root
PYTHON_FINAL_TARGET_DIR="services/savour_rpc" # Final destination relative to root

# --- Helper Function ---
function exit_if() {
    extcode=$1
    msg=$2
    if [ $extcode -ne 0 ]
    then
        if [ "msg$msg" != "msg" ]; then
            echo "Error: $msg" >&2
        fi
        exit $extcode
    fi
}

# --- Main Script Logic ---
echo "Proto Source (Submodule): $PROTO_SRC_DIR"
echo "Intermediate Python Dir: $PYTHON_INTERMEDIATE_DIR"
echo "Final Python Target Dir: $PYTHON_FINAL_TARGET_DIR"

# Create target directory structure and package init files for Python
# Clean up potential old directories first
echo "Cleaning up intermediate directory..."
rm -rf "$PYTHON_INTERMEDIATE_DIR"
exit_if $? "Failed to clean up intermediate directory."

echo "Creating intermediate directory structure..."
mkdir -p "$PYTHON_INTERMEDIATE_DIR"
exit_if $? "Failed to create intermediate directory $PYTHON_INTERMEDIATE_DIR"

# Check if submodule directory exists
if [ ! -d "$PROTO_SUBMODULE_DIR" ] || [ -z "$(ls -A $PROTO_SUBMODULE_DIR)" ]; then
    echo "Error: Submodule directory '$PROTO_SUBMODULE_DIR' not found or empty." >&2
    echo "Please run 'git submodule update --init --recursive' from the project root." >&2
    exit 1
fi

# Find proto files specifically in the dapplink directory
echo "Finding proto files in $PROTO_SRC_DIR..."
protofiles=$(find "$PROTO_SRC_DIR" -name '*.proto')
if [ -z "$protofiles" ]; then
    echo "Error: No proto files found in $PROTO_SRC_DIR" >&2
    exit 1
fi
echo "Found proto files:"
echo "$protofiles"

echo "Compiling python interfaces..."
# Generate Python files
python3 -m grpc_tools.protoc \
       -I "$PROTO_SUBMODULE_DIR" \
       --python_out="$PYTHON_INTERMEDIATE_DIR/" \
       --grpc_python_out="$PYTHON_INTERMEDIATE_DIR/" \
       $protofiles
exit_if $? "Protoc compilation failed."

# Define the path where protoc actually placed the files
protoc_output_subdir="$PYTHON_INTERMEDIATE_DIR/dapplink"

touch "$protoc_output_subdir/__init__.py"
exit_if $? "Failed to create __init__.py in protoc output directory ($protoc_output_subdir)."

# Post-process the generated files to fix import paths
echo "Fixing import paths in generated Python files..."
# Use find + sed to replace 'from dapplink import' with 'from services.savour_rpc import'
find "$protoc_output_subdir/" -name '*.py' -exec sed -i '' 's/^from dapplink import/from services.savour_rpc import/g' {} +
exit_if $? "Failed to fix import paths in generated Python files."

echo "Python compilation finished successfully."

# Sync generated Python code to the final destination
echo "Syncing generated code to final destination: $PYTHON_FINAL_TARGET_DIR"
mkdir -p "$PYTHON_FINAL_TARGET_DIR"
exit_if $? "Failed to create final target directory: $PYTHON_FINAL_TARGET_DIR"

rsync -av --delete "$protoc_output_subdir/" "$PYTHON_FINAL_TARGET_DIR/"
exit_if $? "Failed to sync generated code to $PYTHON_FINAL_TARGET_DIR"

echo "Code sync finished successfully."

# Clean up intermediate directory
echo "Cleaning up intermediate directory..."
rm -rf "$PYTHON_INTERMEDIATE_DIR"
exit_if $? "Failed to remove intermediate directory."

exit 0
