
#VIJETH BALASUBRAMANIAM
#201664207

import random
from datetime import datetime

class BasicAccount:
    acNum = 0
    def __init__(self, acName, openingBalance):
        self.name = acName
        self.balance = openingBalance
        BasicAccount.acNum += 1
        self.acNum = BasicAccount.acNum
        self.cardNum = "".join([str(random.randint(0, 9)) for _ in range(16)])
        self.cardExp = (datetime.now().month, int(str(datetime.now().year)[2:])+3)
    def __str__(self):
        return "Name: "+self.name+"\nAvailable balance: "+str(self.balance)+"\n"+str(self.acNum)+"\n"+str(self.cardNum)+str(self.cardExp)
    def deposit(self, amount=0):
        if amount<0:
            print("Enter valid amount")
            return
        else:
            self.balance += amount
    def withdraw(self, amount=0):
        if self.balance<amount or amount<0:
            print(f"Can not withdraw £{amount}")
            return
        else:
            self.balance -= amount
            print(f"{self.name} has withdrawn £{amount}. New balance is £{self.balance}")
    def getAvailableBalance(self):
        return self.balance
    def getBalance(self):
        return self.balance
    def printBalance(self):
        print("No overdraft for Basic account and balance is",str(self.balance))
    def getName(self):
        return self.name
    def getAcNum(self):
        return str(self.acNum)
    def issueNewCard(self):
        self.cardNum = "".join([str(random.randint(0, 9)) for _ in range(16)])
        self.cardExp = (datetime.now().month, int(str(datetime.now().year)[2:])+3)
    def closeAccount(self):
        self.withdraw(self.balance)
        return True

class PremiumAccount(BasicAccount):
    def __init__(self, acName, openingBalance, intialOverdraft):
        super().__init__(acName, openingBalance)
        self.overdraft = False
        self.overdraftLimit = intialOverdraft
    def __str__(self):
        return "N: "+self.name+"\nAVAILABLE B: "+str(self.balance)+"\nOD "+str(self.overdraftLimit)+"\n"+str(self.acNum)+"\n"+str(self.cardNum)+str(self.cardExp)
    def setOverdraftLimit(self, newLimit):
        self.overdraftLimit = newLimit
    def getAvailableBalance(self):
        return self.balance + self.overdraftLimit if self.overdraftLimit else 0
    def getBalance(self):
        return self.balance
    def withdraw(self, amount=0):
        if amount <= self.balance and amount>0:
            self.balance -= amount
            print(f"{self.name} withdrawn £{amount}.  £{self.balance}")
        elif self.overdraftLimit+self.balance >= amount > 0:
            self.balance -= amount
            self.overdraft = True
            print(f"{self.name} withdrawn £{amount}. £{self.balance}")
        else:
            print(f"Can not withdraw £{amount}")
            return
    def printBalance(self):
        if self.balance >= 0:
            print("Bal", self.balance, "Od", self.overdraftLimit)
        else:
            print("Bal", self.balance, "Od", self.overdraftLimit+self.balance)
    def closeAccount(self):
        if self.balance>=0:
            self.withdraw(self.balance)
            return True
        else:
            print(f"Can not close account,BALANCE £{self.balance*-1}")
        return False