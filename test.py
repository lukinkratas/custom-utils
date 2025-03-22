from custom_utils import track_args, track_time_performance


@track_args
def print_x_ntimes(num: int = 3):
    print(num * 'x')


@track_time_performance(10)
def print_y_ntimes(num: int = 3):
    print(num * 'y')


@track_args
@track_time_performance(10)
def print_z_ntimes(num: int = 3):
    print(num * 'z')


def main():
    print_x_ntimes(num=10)
    print_y_ntimes(num=10)
    print_z_ntimes(10)


if __name__ == '__main__':
    main()
