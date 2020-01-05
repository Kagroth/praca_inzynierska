
import logging

from ServiceCore.solution_executor import *

class PythonExecutor(SolutionExecutor):
    def __init__(self):
        SolutionExecutor.__init__(self)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.testCommand = self.testCommand = ['python', '-m', 'unittest', 'discover', '-v', '-s']

    def configureForExercise(self):
        self.solutionType = SolutionType.objects.get(name=self.solutionData['solutionType'])
        
        if self.solutionType.name == 'File':
            # rozwiazanie nadeslane przez plik
            self.solutionsToRun = self.solutionData['file']

            if self.solutionsToRun is None:
                self.logger.info("Nie podano zadnego pliku")
                return

             # sprawdzanie czy przyslany plik ma poprawne rozszerzenie
            extensionToCheck = self.task.exercise.language.allowed_extension
            
            if not self.solutionsToRun.name.endswith(extensionToCheck):
                self.logger.info("Niepoprawny format pliku")
                return
            
            # iterowanie po wszystkich grupach mimo ze powinna byc tylko jedna
            for group in self.task.assignedTo.all():
                self.fs.location = getUserSolutionPath(self.task, group, self.user)
                # print("A" + self.fs.location)
                self.solutionsToRun.name = 'Solution' + extensionToCheck
                
                destinatedPath = os.path.join(self.fs.location, self.solutionsToRun.name)

                # print("B" + self.fs.location)

                if os.path.isfile(destinatedPath):
                    os.remove(destinatedPath)
                
                self.fs.save(destinatedPath, self.solutionsToRun)
                
                # update command - dodanie lokalizacji self.fs.location do polecenia 
                self.testCommand.append(self.fs.location)
        
        elif self.solutionType.name == 'Editor':
            # rozwiazanie nadeslane przez edytor
            self.solutionsToRun = self.solutionData['solution']
            
            if self.solutionsToRun is None:
                self.logger.info("Nie przyslano rozwiazania")
                return
            
            solutionExtension = self.task.exercise.language.allowed_extension

            # tworze plik z rozwiazaniem
            for group in self.task.assignedTo.all():
                self.fs.location = getUserSolutionPath(self.task, group, self.user)
                print(self.fs.location)
                solutionFileName = 'Solution' + solutionExtension
                
                destinatedPath = os.path.join(self.fs.location, solutionFileName)                

                try:
                    with open(destinatedPath, 'w+') as solution_file:
                        solution_file.write(self.solutionsToRun)
                except Exception as e:
                    self.logger.info("Nie udalo sie zapisac rozwiazania - " + str(e))

        # pobranie sciezki do glownego katalogu cwiczenia i przekopiowanie z niego unit testow
        exercisePath = getExerciseDirectoryRootPath(self.task.exercise)

        self.copyUnitTestsToSolutionDir(exercisePath)

    def copyUnitTestsToSolutionDir(self, exercisePath):
        # kopiowanie unit testow z katalogu Root Exercise do Root Solution
        if os.path.isdir(exercisePath):
            for subdir, dirs, files in os.walk(exercisePath):
                for file in files:
                    if os.path.isfile(os.path.join(subdir, file)):
                        # skopiowanie unit testow
                        copyCommand = 'copy ' + str(os.path.join(subdir, file)) + ' ' + str(os.path.join(self.fs.location, file))
                        print(copyCommand)
                        os.popen(copyCommand)
    
    def run(self):
        newSolution = None

        try:
            with open(os.path.join(self.fs.location, "result.txt"), "w") as result_file:
                self.logger.info(os.getcwd())
                self.logger.info(self.testCommand)
                process = subprocess.run(self.testCommand, capture_output=True, shell=True)
                            
                result_file.write(process.stdout.decode("utf-8"))                           
                result_file.write(process.stderr.decode("utf-8"))

                print(process.stdout.decode("utf-8"))
                print(process.stderr.decode("utf-8"))

                newSolution, created = Solution.objects.update_or_create(task=self.task,
                                                                        user=self.user,
                                                                        pathToFile=self.fs.location,
                                                                        rate=2)
                newSolution.save()
        except Exception as e:
            self.logger.info("Nie udalo sie przetestowac kodu - " + str(e))
            return (False, "Nie udalo sie przetestowac kodu")

        try:
            with open(os.path.join(self.fs.location, "result.txt"), "r") as solution_file:            
                for line in solution_file.readlines():
                    if len(line) == 1:
                        continue
                    self.testsResult.append(line) 
                
        except Exception as e:
            self.logger.info("Nie udalo sie zapisac wynikow testowania")
            return (False, "Nie udalo sie zapisac wynikow")

        self.logger.info("Testowanie rozwiazania pk=" + str(newSolution.pk) + " zakonczone pomyslnie")
        return (True, "Testowanie zakonczone")  