from pyo import *
# from .instruments import RunFm

# You must create and boot a Server before creating any audio object.
RES = 'off'
ATTR = {
    'off': {
        'sr': 44100,
        'bufsize': 512,
        'audio': 'portaudio',
        'fm': 4,
        'sines': 4,
        'wind': 4,
        'punch': 4,
        'strings': 8,
        'bell': 4
    }
}

s = Server(sr=ATTR[RES]['sr'], nchnls=2, buffersize=ATTR[RES]['bufsize'], duplex=0, audio=ATTR[RES]['audio'])
s.boot()
# DURATION = 725
# s.recordOptions(dur=DURATION, filename=sys.argv[1])

# Public Data Attributes of Server:
# amp           float.
# startoffset   float.
# verbosity     int.
# globalseed    int.
s.amp = .13
# s.setStartOffset(300)

### Constants ###
TM = .1125
TAPS = 16
BASS_SEQ = [[3, 3, 6, 4], [6, 6, 4], [3, 3, 2, 8]]
SCALES = [[0, 2, 3, 7, 10], [0, 3, 5, 8, 10], [0, 2, 7, 8, 10]]

### Initialize Timing ###
# minutes = -1
#
#
# def sectionControl():
#     global minutes
#     minutes += 1
#     # if (minutes % 2) == 0:
#     #     print 'Elapsed time: ', minutes/2, 'minutes'
#     if minutes == 1:
#         rSiren.play()
#     elif minutes == 2:
#         rSines.play()
#     elif minutes == 4:
#         rSiren.play()
#     elif minutes == 5:
#         rSines.play()
#     elif minutes == 6:
#         rStringsDuet.play()
#     elif minutes == 8:
#         rBell.activate()
#     elif minutes == 10:
#         rSiren.play()
#     elif minutes == 11:
#         rDisto.openOffSwitch()
#         rPunch.openOffSwitch()
#         rSines.play()
#     elif minutes == 12:
#         sirenSwitch.value = 0
#     elif minutes == 13:
#         rSiren.play()
#     elif minutes == 14:
#         rSines.play()
#         rStrings.play()
#         ampSwitch.value = 0
#         invAmpSwitch.value = 1
#         rBell.openSlowDownSwitch()
#     elif minutes == 17:
#         rKick.stop()
#         rWind.stop()
#         rSines.stop()
#         rSiren.stop()
#     elif minutes == 20:
#         finalFadeout.value = 0
#         fmFinalFadeout.value = 0
#
#
# mainTime = Metro(time=30).play()
# mainFunc = TrigFunc(mainTime, sectionControl)

barTime = Metro(TM * TAPS).play()
barCount = Counter(barTime, max=1000)
eightBarCount = Counter(barTime, max=8)
changeFreqSelect = Select(eightBarCount)
startDisto = Select(barCount, value=[50, 90, 154, 210]).mix(1)
closeDisto = SDelay(startDisto, delay=10.799, maxdelay=11)

countCloseDisto = Counter(closeDisto)
startBell = Select(countCloseDisto, 2)
bassSwitch = Counter(startBell + Trig().play(), min=0, max=2)

ampSwitch = SigTo(value=1, time=60, init=1)
# invAmpSwitch = SigTo(value=0, time=70, init=0)
# fmTranspo = Sig(ampSwitch, mul=.75, add=.25)
# sirenSwitch = SigTo(value=1, time=120, init=1)
# finalFadeout = SigTo(value=1, time=120, init=1)
# fmFinalFadeout = SigTo(value=1, time=90, init=1)

### Processes ###
# rFm = RunFm(TM, TAPS, changeFreqSelect, fmTranspo, countCloseDisto, fmFinalFadeout, bassSwitch, ATTR[RES]['fm'])
rKick = RunKick(TM, TAPS, BASS_SEQ, changeFreqSelect, ampSwitch, bassSwitch, startDisto + closeDisto)
# rDisto = RunDisto(rFm.getOutput(), startDisto)
# rSines = RunHighSines(sirenSwitch, ATTR[RES]['sines'])
# rBell = RunBell(TM, TAPS, startBell, invAmpSwitch, finalFadeout, ATTR[RES]['bell'])
# rNoise = RunNoise()
# rWind = RunWind(rNoise.getOutput(), ampSwitch, countCloseDisto, ATTR[RES]['wind'])
# rSiren = RunSiren(rNoise.getOutput(), sirenSwitch)
# rPunch = RunPunch(rNoise.getOutput(), closeDisto, ATTR[RES]['punch'])
# rStrings = RunStrings(TM, TAPS, SCALES, invAmpSwitch, finalFadeout, ATTR[RES]['strings'])
# rStringsDuet = RunStringsDuet(TM, TAPS, SCALES, ATTR[RES]['strings'])
# rStringsTotal = rStrings.getOut() + rStringsDuet.getOut() + rWind.getOutput() + rSiren.getOutput() + rPunch.getOutput()
# rStringsTotal = rStrings.getOut() + rStringsDuet.getOut()
# rOutRev = WGVerb(Denorm(rStringsTotal), feedback=.95, cutoff=5000, bal=.5, mul=1).out()

### Events callback ###
# x1, thresh1 = 0, 4
#
#
# def callback():
#     global x1, thresh1
#     x1 += 1
#     if (x1 % thresh1) == 0:
#         rKick.change()
#         rFm.change()
#         rBell.change()
#         x1 = 0
#         thresh1 = random.randint(1, 4) * 4


# tt = TrigFunc(rFm.getBarEnd(), callback)

s.start()
# s.gui(locals())
