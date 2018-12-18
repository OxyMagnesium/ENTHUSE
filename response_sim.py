import sys
import time
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
matplotlib.use('TkAgg')

def responseCurve(t):
    return (thrustSetting*0.0104)*(0.0179*(t**5) - 0.4773*(t**4) + 4.0897*(t**3) - 11.2350*(t**2) + 10.8910*(t**1) + 2.4685*(t**0))

def nominalThrust(t):
    if t < 2:
        return responseCurve(2)
    elif t > 8.4:
        return responseCurve(9)
    else:
        return responseCurve(t)

plt.ion()
fig = plt.figure()
ax = plt.subplot(1,1,1)
ax.set_xlabel('Time (s)')
ax.set_ylabel('Value (%)')
ax.set_xlim(left = 0, right = 9)
ax.set_ylim(bottom = 0, top = 110)
timeCoords = []
thrustCoords = []
nominalCoords = []
hydrogenCoords = []
ax.plot(timeCoords, thrustCoords, 'ko-', markersize = 1, color = 'green', label = 'Augmented Thrust')
ax.plot(timeCoords, nominalCoords, 'ko-', markersize = 1, color = 'blue', label = 'Typical Thrust')
ax.plot(timeCoords, hydrogenCoords, 'ko-', markersize = 1, color = 'red', label = 'Hydrogen Flow')
ax.legend(loc = 'upper left')
fig.show()

thrustSetting = input("Enter target thrust setting (%): ")
if thrustSetting == '':
    thrustSetting = 90.0
else:
    thrustSetting = float(thrustSetting)

pause = input("Press enter to start simulation.\n")
del pause

t = 0
hydrogenFlow = 0
previousError = 0
previousTime = 0.001
integralSum = 0
timeStep = 0.05
startTime = time.time()

print("Simulation started.\n")
print("Throttle setting: {0}".format(str(thrustSetting)))

while t < 9:
    t = time.time() - startTime
    hydrogenThrust = 75*hydrogenFlow
    thrust = nominalThrust(t) + hydrogenThrust

    thrustError = thrustSetting - thrust
    hydrogenFlowTarget = 0.096*thrustError + 0.032*(thrustError - previousError)/(t - previousTime)

    flowError = hydrogenFlowTarget - hydrogenFlow
    hydrogenFlow += flowError*0.01
    if hydrogenFlow > 1:
        hydrogenFlow = 1
    elif hydrogenFlow < 0:
        hydrogenFlow = 0

    previousError = thrustError
    previousTime = t

    timeCoords.append(t)
    thrustCoords.append(thrust)
    nominalCoords.append(nominalThrust(t))
    hydrogenCoords.append(hydrogenFlow*100)

    ax.lines[0].set_data(timeCoords, thrustCoords)
    ax.lines[1].set_data(timeCoords, nominalCoords)
    ax.lines[2].set_data(timeCoords, hydrogenCoords)
    ax.relim()
    ax.autoscale_view()
    fig.canvas.flush_events()

    sys.stdout.write("\rThrust: {0}% | Hydrogen Flow: {2} ({3}) | Elapsed time: {1} s".format(round(thrust, 2), round(t, 2), round(hydrogenFlow, 2), round(hydrogenFlowTarget, 2)))
    while time.time() - startTime < timeStep:
        continue
    timeStep += 0.02

pause = input("\n\nPress enter to exit.")
plt.close()
