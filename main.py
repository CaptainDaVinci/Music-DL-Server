from app import app


if __name__ == '__main__':
    from sys import argv
    from app import routes
    print('Starting download for {} {} {}'.format(argv[1], argv[2], argv[3]))
    routes.download_file(argv[1], argv[2], argv[3])
    print('Done')

