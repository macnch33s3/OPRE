def read_ppl_file(file_path):
    """
    read a production planning problem to assign m jobs to n (identical) 
    machines to minimize production time span

    :param file_path:
    :return:
    """
    with open(file_path, 'r') as file:
        num_machines = 0
        job_durations = []
        in_jobs_section = False

        for line in file:
            line = line.strip()
            if line.startswith("NUM_MACHINES"):
                num_machines = int(line.split(":")[1].strip())
            elif line.startswith("NUM_JOBS"):
                continue
            elif line.startswith("JOBS_ID_DURATION"):
                in_jobs_section = True
            elif in_jobs_section and line != "EOF":
                parts = line.split()
                if len(parts) == 2:
                    job_duration = float(parts[1])
                    job_durations.append(job_duration)
            elif line == "EOF":
                break

    return num_machines, job_durations
