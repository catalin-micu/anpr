from os import listdir
from os.path import isfile, join
from controller import Controller

IMAGE_WIDTH = 720
VALID_MENU_COMMANDS = ['1', '2', 'q']
VALID_PLATE_OPTIONS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']

if __name__ == '__main__':
    # app_flag = True
    #
    # while app_flag:
    #     print('\n\n************************** Choose the next action **************************')
    #     print('1 - Detect existing plate')
    #     print('2 - Detect a custom plate')
    #     print('q - Exit')
    #
    #     command = input('Please enter a valid command: ')
    #     while command not in VALID_MENU_COMMANDS:
    #         command = input('Invalid command; Try again: ')
    #
    #     if command == 'q':
    #         app_flag = False
    #
    #     if command == '1':
    #         controller = Controller(IMAGE_WIDTH)
    #         input_plate = input('Choose what plate to detect (number form 1 to 15): ')
    #         while input_plate not in VALID_PLATE_OPTIONS:
    #             input_plate = input('Invalid plate; Try again: ')
    #
    #         image_path = f'images/plate{input_plate}.jpg'
    #         detected_registration_number = controller.run(img_path=image_path)
    #         if detected_registration_number:
    #             print('\n\nDetected number plate:', detected_registration_number)
    #         else:
    #             print('\n\nNo number plate detected.')
    #
    #     if command == '2':
    #         controller = Controller(IMAGE_WIDTH)
    #         input_plate = input('Type the name of the image (must contain file extension): ')
    #         available_images = [f for f in listdir('./images') if isfile(join('./images', f))]
    #
    #         while input_plate not in available_images:
    #             input_plate = input('Invalid plate; Try again: ')
    #
    #         image_path = f'images/{input_plate}'
    #         detected_registration_number = controller.run(img_path=image_path)
    #         if detected_registration_number:
    #             print('\n\nDetected number plate:', detected_registration_number)
    #         else:
    #             print('\n\nNo number plate detected.')

    """
    The section below is meant for algorithm presentation and intermediary results
    """

    controller = Controller(IMAGE_WIDTH)
    detected_registration_number = controller.run(img_path='images/plate5.jpg')

    if detected_registration_number:
        print('Detected number plate:', detected_registration_number)
    else:
        print('No number plate detected.')
