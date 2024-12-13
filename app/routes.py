from flask import Blueprint, request, jsonify
import os

main = Blueprint('main', __name__)
LOG_DIRECTORY = "/var/log"

@main.route('/logs', methods=['GET'])
def fetch_logs():

    filename = request.args.get('filename')
    num_entries = int(request.args.get('num_entries', 10))
    keyword = request.args.get('keyword', '')

    if not filename:
        return jsonify({"error": "Filename is required"}), 400

    file_path = os.path.join(LOG_DIRECTORY, filename)


    if not os.path.isfile(file_path):
        return jsonify({"error": f"File '{filename}' not found in {LOG_DIRECTORY}"}), 404


    logs = []
    try:
        with open(file_path, 'rb') as f:
            f.seek(0, os.SEEK_END)
            file_size = f.tell()
            chunk_size = min(file_size, 1024 * 1024)  


            buffer = b""
            while len(logs) < num_entries and f.tell() > 0:
                to_read = min(chunk_size, f.tell())
                f.seek(-to_read, os.SEEK_CUR)
                buffer = f.read(to_read) + buffer
                f.seek(-to_read, os.SEEK_CUR)
                
                lines = buffer.split(b'\n')
                buffer = lines[0]  
                for line in reversed(lines[1:]):
                    decoded_line = line.decode('utf-8', errors='ignore')
                    if keyword in decoded_line:
                        logs.append(decoded_line)
                        if len(logs) == num_entries:
                            break
            if buffer:
                decoded_line = buffer.decode('utf-8', errors='ignore')
                if keyword in decoded_line:
                    logs.append(decoded_line)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"logs": logs[::-1]})  

