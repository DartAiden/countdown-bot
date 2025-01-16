import discord
import dotenv
import os
import time
from dotenv import load_dotenv
import asyncio
import random
import subprocess
load_dotenv()
from discord.ui import View
roster = []
lettertimer = 30
start = False
activechannels = {}
activeplayers = []

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot(intents=intents)

class game():
    def __init__(self, roster, ctx):
        self.roster = roster
        self.ctx = ctx
        self.scoreboards = {}
        self.chan = ctx

        for user in roster:
            self.scoreboards[user] = game.scoreboard(user)
    def getscoreboards(self):
        return self.scoreboards
        



    class letterbuttons(discord.ui.View):
        def __init__(self, user, word, vowelstatus, consonantstatus, submitstatus, vowelcounter, consonantcounter,round_complete, parent,submit):
            super().__init__() 
            self.timeout = 20
            self.word = word
            self.user = user
            self.consonant_callback.disabled = consonantstatus
            self.vowel_callback.disabled = vowelstatus
            self.submit_callback.disabled = submitstatus
            self.vowelcounter = vowelcounter
            self.consonantcounter=consonantcounter
            self.vowel_callback.disabled = self.vowel_callback.disabled
            self.consonant_callback.disabled = self.consonant_callback.disabled
            self.submit_callback.disabled = self.submit_callback.disabled
            self.round_complete = round_complete
            self.submitted = submit
            self.parent = parent
        def setmessage(self,message):
            self.message = message


        @discord.ui.button(label="Vowel", style=discord.ButtonStyle.primary, row = 0)
        async def vowel_callback(self, button, interaction):
            self.vowelcounter +=1
            self.word = await self.vowelappend(self.word)

            if(self.vowelcounter >= 5 or len(self.word) >= 9):
                self.vowel_callback.disabled = True
            else:
                self.vowel_callback.disabled = False
            if(self.consonantcounter >= 4 and self.vowelcounter >= 3):
                self.submit_callback.disabled = False
            else:
                self.submit_callback.disabled = True
            if(self.consonantcounter >= 6 or len(self.word) >= 9 ):
                self.consonant_callback.disabled = True
            else:
                self.consonant_callback.disabled = False
            await interaction.response.edit_message(view = self, content=f"<@{self.user.id}>! Please choose a consonant or a vowel. Your word is: {(self.word)}")
        @discord.ui.button(label="Consonant", style=discord.ButtonStyle.primary, row = 0)
        async def consonant_callback(self, button, interaction):
            self.consonantcounter +=1
            self.word = await self.consonantappend(self.word)

            if(self.consonantcounter >= 6 or len(self.word) >= 9 ): #I need to fix this logic
                self.consonant_callback.disabled = True
            else:
                self.consonant_callback.disabled = False
            if(self.consonantcounter >= 4 and self.vowelcounter >= 3):
                self.submit_callback.disabled= False
            else:
                self.submit_callback.disabled = True
            if(self.vowelcounter >= 5 or len(self.word) >= 9):
                self.vowel_callback.disabled = True
            else:
                self.vowel_callback.disabled = False
            await interaction.response.edit_message(view =self, content=f"<@{self.user.id}>! Please choose a consonant or a vowel. Your word is: {(self.word)}")
        @discord.ui.button(label="Submit", style=discord.ButtonStyle.primary, row = 0, disabled = True)
        async def submit_callback(self, button, interaction):
                self.submit_callback.disabled= True
                self.vowel_callback.disabled =  True
                self.consonant_callback.disabled = True
                self.submitted = True
                self.stop()
                await interaction.response.edit_message(view = self, content=f"<@{self.user.id}>! Please choose a consonant or a vowel. Your word is: {(self.word)}")
                await self.parent.continueletters(self.word)
        async def on_timeout(self):
            if self.submitted == False:
                self.vowel_callback.disabled = True
                self.consonant_callback.disabled = True
                self.submit_callback.disabled = True
                await self.message.edit(view =self)

                await self.override()


        def chooseconsonant(self):
            seed = random.randrange(0,57)
            if(seed < 1):
                return 'K'
            elif(seed >= 2 and seed < 3):
                return 'J'
            elif(seed >= 3 and seed < 4):
                return 'X'
            elif(seed >= 4 and seed < 5):
                return 'Q'
            elif(seed >= 5 and seed < 6):
                return 'Z'
            elif(seed >= 6 and seed < 8):
                return 'B'
            elif(seed >= 8 and seed < 10):
                return 'C'
            elif(seed >= 10 and seed < 12):
                return 'M'
            elif(seed >= 12 and seed < 14):
                return 'P'
            elif(seed >= 14 and seed < 16):
                return 'F'
            elif(seed >= 16 and seed < 18):
                return 'H'
            elif(seed >= 18 and seed < 20):
                return 'V'
            elif(seed >= 20 and seed < 22):
                return 'W'
            elif(seed >= 22 and seed < 24):
                return 'Y'
            elif(seed >= 24 and seed < 27):
                return 'G'
            elif(seed >= 27 and seed < 31):
                return 'L'
            elif(seed >= 31 and seed < 35):
                return 'S'
            elif(seed >= 35 and seed < 39):
                return 'D'
            elif(seed >= 39 and seed < 45):
                return 'N'
            elif(seed >= 45 and seed < 51):
                return 'R'
            
            else:
                return 'T'    
        async def vowelappend (self, word):
            word += self.choosevowel()
            self.word = word
            return word
        
        def choosevowel(self):
            seed = random.randrange(0,41)
            if(seed < 12):
                return 'E'
            elif(seed >= 12 and seed < 21):
                return 'A'
            elif(seed >= 21 and seed < 30):
                return 'I'
            elif(seed >= 30 and seed < 38):
                return 'O'
            else:
                return 'U'    
        async def consonantappend (self, word):
            word += self.chooseconsonant()
            self.word = word
            return word
        
        def getword(self):
            return self.word
        async def setword(self, word):
            self.word = word

        async def override(self): #overrides user choice and autosubmits when time is up
            if(len(self.getword()) < 7):
                await self.user.send(content = "Time's up! Making auto selection...")
                newlength = random.randrange(7,10)
                while self.vowelcounter < 3:
                    await self.setword(await self.vowelappend(self.getword()))
                    self.vowelcounter +=1
                while self.consonantcounter < 4:
                    await self.setword (await self.consonantappend(self.getword()))
                    self.consonantcounter +=1
                while len(self.getword()) <= newlength:
                    if(random.randrange(1,3) == 1):
                        await self.setword(await self.consonantappend(self.getword()))
                    else:
                        await self.setword(await self.vowelappend(self.getword()))
                await game.continueletters(self.parent, self.getword())
            elif(len(self.getword()) >= 7):
                await self.user.send(content = "Time's up! Submitting..." )
            await game.continueletters(self.parent, self.getword())

    class scoreboard:
        def __init__(self, user):
            self.user = user
            self.score = 0
            self.letterguess = ""
            self.letterguesslength = 0
            self.numberguess = -.5
        def addscore(self, num):
            self.score += num
        def getuser(self):
            return self.user
        def getscore(self):
            return self.score
        def setletterguess(self, letterguess):
            self.letterguess = letterguess
            self.letterguesslength = len(letterguess)
        def setnumberguess(self, numberguess):
            self.numberguess = numberguess
        def getuser(self):
            return self.user
        def getletterguess(self):
            return self.letterguess
        def getletterguesslength(self):
            return self.letterguesslength
        def setnumbersolution(self, solution):
            self.numbersolution = solution
        def getnumbersolution(self):
            return self.numbersolution
    
    async def roundnum(self, game):
        for i in range(5):
            self.round_complete = asyncio.Event()
            await game.letters(i+ 1, game.roster, self.round_complete)
            await self.round_complete.wait()
            
    async def gatherletters(self, user, word, lettertimer, guesslist):
        dmer = user
        self.scoreboards[user].setletterguess("")
        await dmer.send(f"Alright! The word is {str(word)}. You have {lettertimer} seconds. Please reply with your guess:")
        minlength = 0
        def check(message):
            checker = (message.author == dmer and message.channel == dmer.dm_channel)
            return checker
        try:
            end = time.time() + 30
            while time.time() < end:
                remaining = end - time.time() 
                message = await bot.wait_for("message", timeout=remaining, check=check)
                attempt = (message.content).upper()
                if attempt in guesslist:
                    if len(attempt) >= minlength:
                        self.scoreboards.get(user).setletterguess(attempt)
                        await dmer.send(f"Your current guess is {attempt}")
                        minlength = len(attempt)
                    else:
                        await dmer.send("Your previous guess is longer!")
                else:
                    await dmer.send("Invalid guess")
        except asyncio.TimeoutError:
            await dmer.send("Time's up!")

    async def letters(self, round, roster, round_complete):
                for user in roster:
                    await user.send("It's time for letters round " + str(round) + " of 5")

                for user in roster:
                        word = ""
                        letterview = game.letterbuttons(user, word, False, False, True,0,0, round_complete, self, False)
                        usermessage = await user.send(f"<@{user.id}>! Please choose a consonant or a vowel, you have 20 seconds to choose. Your word is:", view = letterview)
                        self.waiterlet = asyncio.Event()
                        done = asyncio.create_task(self.waiterlet.wait())
                        letterview.setmessage(usermessage)
                        await self.waiterlet.wait()
                self.round_complete.set()


    async def continueletters(self, word):
        wordlist = []
        wordlist.append(str(word))
        process = subprocess.Popen(['java', 'solveletters'] + wordlist, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        output = stdout.decode('utf-8')
        guesslist = output.split(",")
        tasklist = []
        for user in self.roster: 
            task = game.gatherletters(self, user, str(word), lettertimer, guesslist)
            tasklist.append(task)
        
        await asyncio.gather(*tasklist)

        lettermax = 0
        lwinnerlist = []
        for user in self.getscoreboards():
            current = self.scoreboards[user].getletterguesslength()
            if(current > lettermax):
                lettermax = current
                lwinnerlist.clear()
                lwinnerlist.append(user)
            elif(current == lettermax):
                lwinnerlist.append(user)
        for user in lwinnerlist:
            self.scoreboards[user].addscore(lettermax)
        if(lettermax == 0):
            for user in self.roster:
                await user.send("No one guessed anything!")
        if(len(lwinnerlist) > 1 and lettermax > 0):
            message = f''' The winners are {lwinnerlist[0]} and {lwinnerlist[1]}, with guesses of {self.scoreboards[lwinnerlist[0]].getletterguess()} and {self.scoreboards[lwinnerlist[1]].getletterguess()}. '''
            for user in self.getscoreboards():
                await user.send(message)
        elif(len(lwinnerlist) > 1 and lettermax != 0):
            for user in self.getscoreboards():
                message  = "The winners are "
                for winner in lwinnerlist:
                    message = message + winner.getuser().display_name + ", "
                    guesses = "with "
                    guess = self.scoreboards[user].getletterguess()
                    guesses = guesses + guess + ", "
                    message = message + guesses
                    message = message + ". They earn " +  str(self.scoreboards[user].getletterguesslength()) + " points."
                await user.send(message)
        else:
        
            message = "The winner is " + lwinnerlist[0].display_name + " with the guess of " + str(self.scoreboards[user].getletterguesslength()) + ". They earn " +  str(self.scoreboards[user].getletterguesslength()) + " points."

            for user in self.getscoreboards():
                await user.send(message)
        guesslist.sort() 
        guesslist.sort(key=len, reverse=True)
        lettermessage = "The solutions are: "
        lettermessage = guesslist[0]
        if len(guesslist) > 100:
            guesslist = guesslist[:100]

        for i in range(len(guesslist)):
            if(i != 0):
                lettermessage = lettermessage + ", " + guesslist[i]
        for user in self.getscoreboards():
            await user.send(lettermessage)
        self.waiterlet.set()


    async def numbernum(self, game):
        for i in range(5):
            await game.numbers(i+ 1, game.roster, game)

    async def numbers(self, round, roster, parent):
        class rootnum():
            def __init__(self, num, index):
                self.val = num
                self.index = index
                self.type = 2
            def toString():
                return str(self.val)
        received = False
        nums = ["1","2","3","4"]

        for user in roster:
            await user.send("It's time for numbers round " + str(round) + " of 5")
        for user in roster:
            def check(message):
                checker = (message.author == user and message.channel == user.dm_channel)
                return checker
            await user.send(f"<@{user.id}> Please choose the number of large numbers you'd like to include in your guess, between 0 and 4 inclusive. You have 30 seconds.")
            try:
                while True:
                    message = await bot.wait_for("message", timeout = 30.0, check = check)
                    if message.content in nums:
                        number = int(message.content)
                        numlist = parent.numslist(number)
                        received == True
                        break
                    else:
                        await user.send("Invalid guess.")
            except asyncio.TimeoutError:
                if received == False:
                    await user.send("Time's up! Picking numbers randomly...")
                    numlist = parent.numslist(random.randrange(0,4))
            self.received = {player: False for player in self.roster}

            self.all_submit = asyncio.Event()
            self.waiter = asyncio.create_task(self.all_submit.wait())  
            target = random.randrange(1,1000)

            for user in roster:

                rootlist = []
                for i in range(len(numlist)):
                    newnum = rootnum(numlist[i], i)
                    rootlist.append(newnum)
                await user.send(f"Alright! The numbers are {numlist[0]}, {numlist[1]}, {numlist[2]}, {numlist[3]}, {numlist[4]}, and {numlist[5]}. You have 40 seconds. The target number is **{target}**. Once you submit an answer, you cannot change it.", view = parent.numbuttons(user, rootlist, target, [],[], time.time() + 40, [], parent, [-.5, -.5, -.5, -.5],False))
            timer1 = asyncio.create_task(asyncio.sleep(40))
            self.consubmit = asyncio.Event()
            self.waiter = asyncio.create_task(self.all_submit.wait())  
            done, pending = await asyncio.wait([self.waiter, timer1],return_when=asyncio.FIRST_COMPLETED,)
            mindiff = 1000
            winnerlist = []
            for user in roster:
                if abs(self.scoreboards[user].numberguess - target) <= mindiff:
                    if abs((self.scoreboards[user].numberguess - target)) < mindiff:
                        mindiff = abs((self.scoreboards[user].numberguess - target))
                        winnerlist.clear()
                    winnerlist.append(user)
            for user in roster:
                if mindiff == 0:
                    self.scoreboards[user].addscore(10)
                    earned = 10
                elif mindiff >= 1 and mindiff <= 5:
                    self.scoreboards[user].addscore(7)
                    earned = 7
                elif mindiff >=5 and mindiff <= 10:
                    self.scoreboards[user].addscore(5)
                    earned = 5
                else: earned = 0
            if len(winnerlist) == 1:
                mess = f"The winner is {winnerlist[0].display_name}, and they earn {earned} points! They have the solution: \n {self.scoreboards[winnerlist[0]].numbersolution}"
            elif len(winnerlist) == 2:
                mess = f"The winners are {winnerlist[0].display_name} and {winnerlist[1].display_name}, and they earn {earned} points! Respectively, they have the solutions: \n {self.scoreboards[winnerlist[0]].solution} \n and: \n {self.scoreboards[winnerlist[1]].solution}"
            else:
                mess = f"Earning {earned} points, the winners are "
                for i in range(len(winnerlist)-1):
                    mess+= str(winnerlist[0].display_name) + ", "
                mess+= f"and {winnerlist[-1].display_name}"
            for user in roster:
                await user.send(mess)
            inputlist = []
            for i in numlist:
                inputlist.append(str(i))
            inputlist.append(str(target))
            process = subprocess.Popen(['java', 'solvenumbers'] + inputlist, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            output = stdout.decode('utf-8')
            outputlist = output.split('BREAK')
            if len(outputlist)> 10:
                outputlist = outputlist[:10]
            newmess = "Some of the other solutions include: \n"
            for i in outputlist:
                newmess += i
                newmess += "\n"
            for user in roster:
                await user.send(newmess)
            for user in roster:
                self.scoreboards[user].setnumberguess(1000)
                self.scoreboards[user].setnumbersolution("")
        
    
            





    def checkall(self, user):
        self.received[user] = True
        if all(self.received.values()): 
            self.all_submit.set()




    def numslist(self, num):
        def randchooser(list):
            item = list[random.randrange(0,len(list))]
            list.remove(item)
            finallist.append(item)
            return list
        
        smallnums = []
        largenums = []
        for i in range(10):
            smallnums.extend([i+1] * 2)
        for i in range(4):
            largenums.extend([(i+1)*25])
        finallist = []
        for i in range(num):
            randchooser(largenums)
        for i in range(6-num):
            randchooser(smallnums)
        return finallist 

    class numbuttons(discord.ui.View):
        class equation():
            def __init__(self, num1, operation, num2):
                class num():
                    def __init__(self, ind, val ):
                        self.index = ind
                        self.val = val


                self.ops = {1: "+",
                        2: "-",
                        3: "*",
                        4: "/"}
                self.num1 = num1
                self.operation = operation
                self.num2 = num2
                self.type = 0 # 0 means equation
                self.result = num(-1, 0)
                if operation == 1:
                    self.result.val = num1.val + num2.val
                elif operation == 2:
                    self.result.val = num1.val - num2.val
                elif operation == 3:
                    self.result.val = num1.val * num2.val
                elif operation == 4:
                    self.result.val = num1.val / num2.val
            def toString(self):
                return f"{self.num1.val} {self.ops[self.operation]} {self.num2.val} = {self.result.val}"
            def toList(self):
                return [self.num1, self.operation, self.num2]


        class rootnums:
            def __init__(self, val, equations, index, children):
                self.val = val
                self.equations = equations
                self.index = index
                self.type = 1
                self.children = children
            def toString(self):
                if len(self.equations) > 0:
                    lister = []
                    for n in self.equations:
                        lister.append(n.toString())
                    return '\n'.join(lister)
                else:
                    return str(self.val)
        

        def __init__(self, user, nums, target, memo, current, timer, indices, parent, mems, submit):
            super().__init__()

            self.user = user
            self.nums = nums
            self.memo = memo
            self.current = current
            self.timeout = timer - time.time()
            self.indices = indices
            self.parent = parent
            self.target = target
            self.mems = mems
            self.timer = timer
            self.submit = submit
            self.button1_callback.label = nums[0].val
            self.button2_callback.label = nums[1].val
            self.button3_callback.label = nums[2].val
            self.button4_callback.label = nums[3].val
            self.button5_callback.label = nums[4].val
            self.button6_callback.label = nums[5].val
            self.refreshnums()

        async def submitter(self):
                self.submit = True
                self.parent.checkall(self.user)
                self.parent.scoreboards[self.user].setnumberguess(self.current[0].val)
                self.refreshnums()
                await self.message.edit(view = self)
        def refreshnums(self):
            if self.mems[0] == -.5:
                self.mem1_callback.label = "Mem 1"
                self.clear1_callback.disabled = True
            else:
                self.mem1_callback.label = str(self.mems[0].val)
                if self.mems[0].index not in self.indices:
                    self.clear1_callback.disabled = False
                else:
                    self.clear1_callback.disabled = True
            if self.mems[1] == -.5:
                self.mem2_callback.label = "Mem 2"
                self.clear2_callback.disabled = True
            else:
                self.mem2_callback.label = str(self.mems[1].val)
                if self.mems[1].index not in self.indices:
                    self.clear2_callback.disabled = False
                else:
                    self.clear2_callback.disabled = True
                
            if self.mems[2] == -.5:
                self.mem3_callback.label = "Mem 3"
                self.clear3_callback.disabled = True
            else:
                self.mem3_callback.label = str(self.mems[2].val)
                if self.mems[2].index not in self.indices:
                    self.clear3_callback.disabled = False
                else:
                    self.clear3_callback.disabled = True

            if self.mems[3] == -.5:
                self.mem4_callback.label = "Mem 4"
                self.clear4_callback.disabled = True
            else:
                self.mem4_callback.label = str(self.mems[3].val)
                if self.mems[3].index not in self.indices:
                    self.clear4_callback.disabled = False
                else:
                    self.clear4_callback.disabled = True
                
            if len(self.memo) == 0 and len(self.current) == 0: #Opening state
                self.button1_callback.disabled = self.nums[0].index in self.indices
                self.button2_callback.disabled = self.nums[1].index in self.indices
                self.button3_callback.disabled = self.nums[2].index in self.indices
                self.button4_callback.disabled = self.nums[3].index in self.indices
                self.button5_callback.disabled = self.nums[4].index in self.indices
                self.button6_callback.disabled = self.nums[5].index in self.indices
                self.add_callback.disabled = True
                self.subtract_callback.disabled = True
                self.multiply_callback.disabled = True
                self.divide_callback.disabled = True
                self.delete_callback.disabled = True
                self.submit_callback.disabled = True
                if self.mems[0] == -.5 or self.mems[0].index in self.indices:
                    self.mem1_callback.disabled = True
                else:
                    self.mem1_callback.disabled = False  
                if self.mems[1] == -.5 or self.mems[1].index in self.indices:
                    self.mem2_callback.disabled = True
                else:
                    self.mem2_callback.disabled = False  
                if self.mems[2] == -.5 or self.mems[2].index in self.indices:
                    self.mem3_callback.disabled = True
                else:
                    self.mem3_callback.disabled = False  

                if self.mems[3] == -.5 or self.mems[3].index in self.indices:
                    self.mem4_callback.disabled = True
                else:
                    self.mem4_callback.disabled = False  

            elif len(self.current) == 1:#entering operators

                self.button1_callback.disabled = True
                self.button2_callback.disabled = True
                self.button3_callback.disabled = True
                self.button4_callback.disabled = True
                self.button5_callback.disabled = True
                self.button6_callback.disabled = True
                self.add_callback.disabled = False
                self.subtract_callback.disabled = False
                self.multiply_callback.disabled = False
                self.divide_callback.disabled = False
                self.delete_callback.disabled = False
                self.submit_callback.disabled = False
                if self.mems[0] == -.5 :
                    self.mem1_callback.disabled = False
                else:
                    self.mem1_callback.disabled = True          
                if self.mems[1] == -.5 :
                    self.mem2_callback.disabled = False
                else:
                    self.mem2_callback.disabled = True   
                if self.mems[2] == -.5:
                    self.mem3_callback.disabled = False
                else:
                    self.mem3_callback.disabled = True          

                if self.mems[3] == -.5:
                    self.mem4_callback.disabled = False
                else:
                    self.mem4_callback.disabled = True

            elif len(self.current) == 2 and self.current[1] != 4: #entering current num
                self.button1_callback.disabled = self.nums[0].index in self.indices
                self.button2_callback.disabled = self.nums[1].index in self.indices
                self.button3_callback.disabled = self.nums[2].index in self.indices
                self.button4_callback.disabled = self.nums[3].index in self.indices
                self.button5_callback.disabled = self.nums[4].index in self.indices
                self.button6_callback.disabled = self.nums[5].index in self.indices
                self.add_callback.disabled = True
                self.subtract_callback.disabled = True
                self.multiply_callback.disabled = True
                self.delete_callback.disabled = False
                self.submit_callback.disabled = True
                self.mem1_callback.disabled = True
                if self.mems[0] == -.5 or self.mems[0].index in self.indices:
                    self.mem1_callback.disabled = True
                else:
                    self.mem1_callback.disabled = False  
                if self.mems[1] == -.5 or self.mems[1].index in self.indices:
                    self.mem2_callback.disabled = True
                else:
                    self.mem2_callback.disabled = False  
                if self.mems[2] == -.5 or self.mems[2].index in self.indices:
                    self.mem3_callback.disabled = True
                else:
                    self.mem3_callback.disabled = False  

                if self.mems[3] == -.5 or self.mems[3].index in self.indices:
                    self.mem4_callback.disabled = True
                else:
                    self.mem4_callback.disabled = False  

            elif len(self.current) == 2 and self.current[1] == 4: #entering current num
                self.button1_callback.disabled = self.nums[0].index in self.indices and self.current[0].val % self.nums[0].val == 0
                self.button2_callback.disabled = self.nums[1].index in self.indices and self.current[0].val % self.nums[1].val == 0
                self.button3_callback.disabled = self.nums[2].index in self.indices and self.current[0].val % self.nums[2].val == 0
                self.button4_callback.disabled = self.nums[3].index in self.indices and self.current[0].val % self.nums[3].val == 0
                self.button5_callback.disabled = self.nums[4].index in self.indices and self.current[0].val % self.nums[4].val == 0
                self.button6_callback.disabled = self.nums[5].index in self.indices and self.current[0].val % self.nums[5].val == 0
                self.add_callback.disabled = True
                self.subtract_callback.disabled = True
                self.multiply_callback.disabled = True
                self.delete_callback.disabled = False
                self.submit_callback.disabled = True
                self.mem1_callback.disabled = True
                if self.mems[0] == -.5 or self.mems[0].index in self.indices or self.current[0] % self.mems[0].val != 0:
                    self.mem1_callback.disabled = True
                else:
                    self.mem1_callback.disabled = False
                if self.mems[1] == -.5 or self.mems[1].index in self.indices or self.current[0] % self.mems[1].val != 0:
                    self.mem2_callback.disabled = True
                else:
                    self.mem2_callback.disabled = False
                if self.mems[2] == -.5 or self.mems[2].index in self.indices or self.current[0] % self.mems[2].val != 0:
                    self.mem3_callback.disabled = True
                else:
                    self.mem3_callback.disabled = False  

                if self.mems[3] == -.5 or self.mems[3].index in self.indices or self.current[0] % self.mems[3].val != 0:
                    self.mem4_callback.disabled = True
                else:
                    self.mem4_callback.disabled = False  
            if self.submit == True:
                self.button1_callback.disabled = True
                self.button2_callback.disabled = True
                self.button3_callback.disabled = True
                self.button4_callback.disabled = True
                self.button5_callback.disabled = True
                self.button6_callback.disabled = True
                self.add_callback.disabled = True
                self.subtract_callback.disabled = True
                self.multiply_callback.disabled = True
                self.divide_callback.disabled = True
                self.delete_callback.disabled = True
                self.submit_callback.disabled = True
                self.clear1_callback.disabled = True
                self.clear2_callback.disabled = True
                self.clear3_callback.disabled = True
                self.clear4_callback.disabled = True
                self.mem1_callback.disabled = True
                self.mem2_callback.disabled = True
                self.mem3_callback.disabled = True
                self.mem4_callback.disabled = True
        async def main_on_timeout(self):
            if self.user.numberguess == -5:
                await self.user.send("Time's up! Setting last entered number as guess...")
                await self.submitter()
                if len(self.current > 0):
                    self.user.numberguess = self.current[0]
                await self.message.edit(view = self)

        @discord.ui.button(label="button1", style=discord.ButtonStyle.primary, row = 0, disabled = False)
        async def button1_callback(self, button, interaction):
            self.load(self.nums[0])
            self.indices.append(0)
            self.refreshnums()
            await interaction.response.edit_message(content = str(self.prepmessage()), view = self)
        @discord.ui.button(label="button2", style=discord.ButtonStyle.primary, row = 0, disabled = False)
        async def button2_callback(self, button, interaction):
            self.load(self.nums[1])
            self.indices.append(1)
            self.refreshnums()

            await interaction.response.edit_message(content = str(self.prepmessage()), view = self)
        @discord.ui.button(label="button3", style=discord.ButtonStyle.primary, row = 0, disabled = False)
        async def button3_callback(self, button, interaction):
            self.load(self.nums[2])
            self.indices.append(2)
            self.refreshnums()
            await interaction.response.edit_message(content = str(self.prepmessage()), view = self)
        @discord.ui.button(label="button4", style=discord.ButtonStyle.primary, row = 1, disabled = False)
        async def button4_callback(self, button, interaction):
            self.load(self.nums[3])
            self.indices.append(3)
            self.refreshnums()
            await interaction.response.edit_message(content = str(self.prepmessage()), view = self)
        @discord.ui.button(label="button5", style=discord.ButtonStyle.primary, row = 1, disabled = False)
        async def button5_callback(self, button, interaction):
            self.load(self.nums[4])
            self.indices.append(4)
            self.refreshnums()
            await interaction.response.edit_message(content = str(self.prepmessage()), view = self)
        @discord.ui.button(label="button6", style=discord.ButtonStyle.primary, row = 1, disabled = False)
        async def button6_callback(self, button, interaction):
            self.load(self.nums[5])
            self.indices.append(5)
            self.refreshnums()
            await interaction.response.edit_message(content = str(self.prepmessage()), view = self)
        @discord.ui.button(label="+", style=discord.ButtonStyle.primary, row = 0, disabled = True)
        async def add_callback(self, button, interaction):
            self.load(1)
            self.refreshnums()
            await interaction.response.edit_message(content = str(self.prepmessage()), view = self)
        @discord.ui.button(label="-", style=discord.ButtonStyle.primary, row = 0, disabled = True)
        async def subtract_callback(self, button, interaction):
            self.load(2)
            self.refreshnums()
            await interaction.response.edit_message(content = str(self.prepmessage()), view = self)
        @discord.ui.button(label="*", style=discord.ButtonStyle.primary, row = 1, disabled = True)
        async def multiply_callback(self, button, interaction):
            self.load(3)
            self.refreshnums()
            await interaction.response.edit_message(content = str(self.prepmessage()), view = self)
        @discord.ui.button(label="/", style=discord.ButtonStyle.primary, row = 1, disabled = True)
        async def divide_callback(self, button, interaction):
            self.load(4)
            self.refreshnums()
            await interaction.response.edit_message(content = str(self.prepmessage()), view = self)
        @discord.ui.button(label="Submit", style=discord.ButtonStyle.primary, row = 2, disabled = True)
        async def submit_callback(self, button, interaction):
            self.parent.scoreboards[self.user].setnumberguess(self.current[0].val)
            self.ops = {1: "+",
                        2: "-",
                        3: "*",
                        4: "/"}
            temp = []
            for i in self.mems:
                if hasattr(i, 'val'):
                    temp.append(i.toString())
            for i in self.memo:
                temp.append(i.toString())
            if len(self.current) >0:
                temps = ""
                if len(self.current ) >= 1:
                    if hasattr(self.current[0], 'val'):
                        temps+=str(self.current[0].val) + " "
                    else:
                        temps+=str(self.current[0]) + " "
                if len(self.current) == 2:
                    temps+= str(self.ops[self.current[1]])
                temp.append(temps)
                self.parent.scoreboards[self.user].setnumbersolution('\n'.join(temp))   
            await self.submitter()
            self.refreshnums()
            await interaction.response.edit_message(content = str(self.prepmessage()), view = self)
        @discord.ui.button(label="Delete", style=discord.ButtonStyle.primary, row = 2, disabled = True)

        async def delete_callback(self, button, interaction):
            self.deleter()
            self.refreshnums()
            await interaction.response.edit_message(content = str(self.prepmessage()), view = self)

        @discord.ui.button(label = "Mem1", style = discord.ButtonStyle.primary, row = 3, disabled = True)
        async def mem1_callback(self, button, interaction):
            self.addmem(0)
            self.refreshnums()
            await interaction.response.edit_message(content = str(self.prepmessage()), view = self)
        @discord.ui.button(label = "Mem2", style = discord.ButtonStyle.primary, row = 3, disabled = True)

        async def mem2_callback(self, button, interaction):
            self.addmem(1)
            self.refreshnums()
            await interaction.response.edit_message(content = str(self.prepmessage()), view = self)
        @discord.ui.button(label = "Mem3", style = discord.ButtonStyle.primary, row = 3, disabled = True)

        async def mem3_callback(self, button, interaction):
            self.addmem(2)
            self.refreshnums()
            await interaction.response.edit_message(content = str(self.prepmessage()), view = self)
        @discord.ui.button(label = "Mem4", style = discord.ButtonStyle.primary, row = 3, disabled = True)

        async def mem4_callback(self, button, interaction):
            self.addmem(3)
            self.refreshnums()
            await interaction.response.edit_message(content = str(self.prepmessage()), view = self)
        @discord.ui.button(label = "Clear 1", style = discord.ButtonStyle.primary, row = 4, disabled = True)
        async def clear1_callback(self, button, interaction):
            self.delmem(0)
            self.refreshnums()
            await interaction.response.edit_message(content = str(self.prepmessage()), view = self)
        
        @discord.ui.button(label = "Clear 2", style = discord.ButtonStyle.primary, row = 4, disabled = True)
        async def clear2_callback(self, button, interaction):
            self.delmem(1)
            self.refreshnums()
            await interaction.response.edit_message(content = str(self.prepmessage()), view = self)

        @discord.ui.button(label = "Clear 3", style = discord.ButtonStyle.primary, row = 4, disabled = True)
        async def clear3_callback(self, button, interaction):
            self.delmem(2)
            self.refreshnums()
            await interaction.response.edit_message(content = str(self.prepmessage()), view = self)
    
        @discord.ui.button(label = "Clear 4", style = discord.ButtonStyle.primary, row = 4, disabled = True)
        async def clear4_callback(self, button, interaction):
            self.delmem(3)
            self.refreshnums()
            await interaction.response.edit_message(content = str(self.prepmessage()), view = self)
        def load(self, numval):
            self.current.append(numval)
            if len(self.current) == 3:
                curr = self.equation(*self.current)
                self.memo.append(curr)
                self.current = []
                self.current.append(curr.result)
                
        def deleter(self):
            if len(self.current) == 2:
                self.current.pop()
            elif len(self.memo) == 0 and (len(self.current)==1):
                self.indices.remove(self.current[-1].index)
                self.current.pop()
            else:
                temp = self.memo.pop().toList()
                self.indices.remove(temp[-1].index)
                self.current = temp[:2]

        def addmem(self, ind):
            if self.mems[ind] == -.5:
                current = self.rootnums(self.current[0].val, self.memo.copy(), ind+6, self.indices.copy())
                self.current.clear()
                self.memo.clear()
                self.mems[ind] = current
            else:
                self.indices.append(ind+6)
                self.load(self.mems[ind])

        def delmem(self, ind):
            current = self.mems[ind]
            for i in current.children:
                if isinstance(i, list):
                    for j in i:
                        if j > 5:
                            self.mems[j-6] = -.5
                        self.indices.remove(j)
                        
                else:
                    self.indices.remove(i)
                    if i > 5:
                        self.mems[i - 6] = -.5
            self.mems[ind] = -.5

        def prepmessage(self):
            self.ops = {1: "+",
                        2: "-",
                        3: "*",
                        4: "/"}
            temp = [f"Alright! The numbers are {self.nums[0].val}, {self.nums[1].val}, {self.nums[2].val}, {self.nums[3].val}, {self.nums[4].val}, and {self.nums[5].val}. You have 40 seconds. The target number is **{self.target}**. Once you submit an answer, you cannot change it."]
            for i in self.mems:
                if hasattr(i, 'val'):
                    temp.append(i.toString())
            for i in self.memo:
                temp.append(i.toString())
            if len(self.current) >0:
                temps = ""
                if len(self.current ) >= 1:
                    if hasattr(self.current[0], 'val'):
                        temps+=str(self.current[0].val) + " "
                    else:
                        temps+=str(self.current[0]) + " "
                if len(self.current) == 2:
                    temps+= str(self.ops[self.current[1]])
                temp.append(temps)
            return '\n'.join(temp)   
        
    async def conundrum(self, newgame):
        process = subprocess.Popen(['java', 'solveconundrum'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        output = stdout.decode('utf-8')
        self.cor = 0

        outputs = output.split(",")
        conundrum = outputs[0]
        ans = outputs[1].strip()
        tasklist = []
        self.conall_submit = asyncio.Event()
        self.conwaiter = asyncio.create_task(self.conall_submit.wait())  
        for user in self.roster:
            await user.send(f'The conundrum is {conundrum}.')
            tasklist.append (game.gatheranswers(self, user, ans),)
        await asyncio.gather(*tasklist)
        timer1 = asyncio.create_task(asyncio.sleep(40))
        done, pending = await asyncio.wait([self.conwaiter, timer1],return_when=asyncio.FIRST_COMPLETED,)
        if self.cor != 0:
            for user in self.roster:
                await user.send(f"The winner of the conundrum is {self.cor}! They win 9 points! The answer was {ans}.")
                self.scoreboards[self.cor].addscore(9)
        else:
            for user in self.roster:
                await user.send(f"There are no winners! The answer was {ans}.")
            


            
    async def gatheranswers(self, user, ans):
        def check(message):
            return (message.author == user and message.channel == user.dm_channel and (message.content.startswith("bz") or message.content.startswith("buzz")))
        msg = await bot.wait_for('message', check=check)
        if msg.content.startswith("bz"):
            cont = msg.content[2:]
        if msg.content.startswith("buzz"):
            cont = msg.content[4:]
        print(cont.strip().upper())
        if cont.strip().upper() == ans:
            self.cor = user

            self.conall_submit.set()
        else:
            await user.send("Invalid guess! Your turn has ended!")

    async def finish(self):
        winnerlist = []
        minscore = -1
        for user in self.roster:
            if self.scoreboards[user].score >= minscore:
                if self.scoreboards[user].score > minscore:
                    winnerlist.clear()
                    minscore = self.scoreboards[user].score
                winnerlist.append(user)
        if len(winnerlist) == 1:
            for user in self.roster:
                await user.send(f"The winner is {winnerlist[0].display_name}, with a score of {self.scoreboards[winnerlist[0]].score}.")
        elif len(winnerlist) == 2:
            for user in self.roster:
                await user.send((f"The winnes are {winnerlist[0].display_name} and {winnerlist[1].display_name}, with a score of {self.scoreboards[winnerlist[0]].score}."))
        else:
            mess = f"With a score of {self.scoreboards[winnerlist[0]].score}, the winners are "
            for i in range(len(winnerlist)-1):
                mess+= str(winnerlist[0].display_name) + ", "
            mess+= f"and {winnerlist[-1].display_name}"
            for user in self.roster:
                await user.send(mess)

        message = ""
        scorelist = []
        for user in self.roster:
            scorelist.append(user)
        scorelist.sort(key = lambda user: self.scoreboards[user].score)
        for user in scorelist:
            username = user.display_name
            score = self.scoreboards[user].score
            message = message + f"""{username}: {score} points \n"""
        for user in self.roster:
            await user.send(message)
        global activechannels
        del activechannels[self.chan.channel]



            

                
@bot.slash_command(name="score", description="returns score")
async def score(ctx: discord.ApplicationContext):
    global activechannels
    if(ctx.channel not in activechannels):
        await ctx.send("The game has not started!")
    else:
        message = ""
        scorelist = []
        for user in activechannels[ctx.channel].scoreboards:
            scorelist.append(user)
        scorelist.sort(key = lambda it: activechannels[ctx.channel].scoreboards[user].score)
        for user in scorelist:
            username = (user).display_name
            score = activechannels[ctx.channel].scoreboards[user].score
            message = message + f"""{username}: {score} points \n"""
            await ctx.send(message)

"""
@bot.slash_command(name="end", description="end")
async def end(ctx: discord.ApplicationContext):
    global activechannels
    if ctx.channel in activechannels:
        await ctx.send("Game ended!")
        del activechannels[ctx.channel]
        return 0
    else:
        await ctx.send("There is no ongoing game!")
"""

@bot.slash_command(name="help", description="help menu")
async def help(ctx: discord.ApplicationContext):
    await ctx.respond("This is a Discord bot to help users play the British game show Countdown. Simply type /start to enter a game. Feel free to message me @ AachenFur to contact me.")

@bot.slash_command(name="start", description="start")
async def start(ctx: discord.ApplicationContext):
    async def initializegame():
        newgame = game(roster, ctx)
        activechannels[ctx.channel] = newgame
        for user in roster:
            await user.send(f"It's time for the letters round. A word must have at least 3 vowels and 4 consonants. A word has a maximum of 9 letters.")

        await newgame.roundnum(newgame)
        for user in roster:
            await user.send("It's time for the numbers round. Please choose how many large numbers you want. The remaining will be small numbers")
        await newgame.numbernum(newgame)
        for user in roster:
            await user.send("It's time for counundrum! Please type 'buzz' or 'bz' followed by your answer. You have one guess as to what the unscrambled 9-letter word is.")
        await newgame.conundrum(newgame)
        await newgame.finish()
    global activechannels
    if ctx.channel in activechannels:
        await ctx.send("The game is already in progress.")
    else:
        timer = time.time()+15

        roster = []
        startmsg = await ctx.send("""Please type `!join` to join the game or `!leave` to leave. 
The game will start in 20 seconds. The following players have joined:""")

        def check(msg):
            return msg.channel == ctx.channel and msg.content.lower() in ["!join", "!leave"]
        while time.time()  < timer:
            timeout = asyncio.create_task(asyncio.sleep(timer - time.time()))
            message_task = asyncio.create_task(bot.wait_for("message", check=check))
            
            done, pending = await asyncio.wait(
                [message_task, timeout],
                return_when=asyncio.FIRST_COMPLETED
            )

            for task in pending:
                task.cancel()

            if message_task in done:
                msg = message_task.result()
                if msg.content.lower() == "!join" and msg.author not in roster:
                    roster.append(msg.author)
                elif msg.content.lower() == "!leave" and msg.author in roster:
                    roster.remove(msg.author)

                await startmsg.edit(content=f"""Please type `!join` to join the game or `!leave` to leave. 
The game will start in 20 seconds. The following players have joined:
{"\n".join([user.display_name for user in roster])}""")
        if len(roster) == 0:
            await ctx.send("No one joined the game!")
            del activechannels[ctx.channel]
        else:
            await ctx.send(f"Starting... Please make sure the bot can DM you.")
            await initializegame()



@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
    global activechannels
    activechannels.clear()

dotenv.load_dotenv()
token = str(os.getenv("TOKEN"))
bot.run(os.getenv('TOKEN'))
