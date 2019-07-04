import get_all_jain_index
import rtt_convert_log_to_point

def main():
    rtt_convert_log_to_point.get_rtt3()
    rtt_convert_log_to_point.get_rtt4()

    get_all_jain_index.merge_files_in_path(get_all_jain_index.PATH1)
    get_all_jain_index.merge_files_in_path(get_all_jain_index.PATH2)

if __name__ == '__main__':
    main()
