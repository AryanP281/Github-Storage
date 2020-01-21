#*****************************************Imports*********************************
from github import Github

#***********************************Classes*******************************
class GithubStorage(object) :
    ghb = None #Connection to the github account
    repo = None #The repository acting as the storage
    
    def __init__(self, login_credentials):

        #Connecting to the github account
        self.connect_to_account(login_credentials)

    def connect_to_repo(self, repo_name) :
        """Connects to the repository acting as the server"""

        try:
            self.repo = ghb.get_repo(repo_name)
        except :
            raise Exception(f'Unable to connect to repository "{repo_name}"')

    def connect_to_account(self, login_credentials) :
        """Connects to the given github account"""

        try :
            self.ghb = Github(login_credentials[0], login_credentials[1])
        except :
            raise Exception("Unable to connect to github account")

    def create_file(self, file_path, file_data="", branch="master") :
        """Creates a file in the repo and returns 0 if file-creation is successful. Else returns -1"""

        #Creating the file
        try:
            self.repo.create_file(file_path, f"Created file {file_path}", file_data, branch=branch)
            return 0
        except :
            return -1

    def delete_file(self, file_path, branch="master") :
        """Deletes the given file from the repository. Returns 0 is successful else -1. 
        file_path should not contain the file extension i.e test.txt = test"""

        #Deleting the file
        try:
            file = self.repo.get_contents(file_path) #Getting file info
            self.repo.delete_file(file.path, f"Deleted file {file_path}", file.sha, branch=branch) #Deleting the file
            return 0
        except :
            return -1

    def get_file(self, file_path) :
        """Returns the given file i.e a ContentFile object
        file_path should not contain the file extension i.e test.txt = test"""

        try :
            return self.repo.get_contents(file_path)
        except :
            return None

    def get_file_data(self, file_path) :
        """Returns the data in the given file
        file_path should not contain the file extension i.e test.txt = test"""

        try :
            return self.repo.get_contents(file_path).decoded_content
        except :
            return None

    def write_to_file(self, file_path, data, append=False, branch="master") :
        """Writes the data to the given file
        file_path should not contain the file extension i.e test.txt = test"""

        try :
            #Checking if the data is to be appended or the file is to be truncated
            if(append) :
                file = self.get_file(file_path) #Getting an instance to the file 
                old_data = str(file.decoded_content) #Getting the old data in string form
                new_data = old_data + str(data) #Adding the old data and the appended data
                #Updating the file
                self.repo.update_file(file.path, f'Updated file {file_path}', new_data, file.sha, branch=branch)
            else :
                file = self.get_file(file_path) #Getting an instance to the file 
                #Updating the file
                self.repo.update_file(file.path, f'Updated file {file_path}', data, file.sha, branch=branch)
        except :
            raise Exception("Unable to write to file")






