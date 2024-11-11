from pytrovich.detector import PetrovichGenderDetector

detector = PetrovichGenderDetector()
print(detector.detect(firstname="Иван"))  # Gender.MALE
print(detector.detect(firstname="Роман", middlename="Александрович"))  # Gender.MALE
print(detector.detect(firstname="Арзу", middlename="Лутфияр кызы"))  # Gender.FEMALE

