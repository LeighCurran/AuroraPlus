import auroraplus
AuroraPlus = auroraplus.api("leigh.curran@outlook.com", "MuCEiD49%3Z%&y")
AuroraPlus.getsummary()

print(AuroraPlus.DollarValueUsage['T41'])
print(AuroraPlus.DollarValueUsage['T31'])
print(AuroraPlus.DollarValueUsage['Other'])
print(AuroraPlus.DollarValueUsage['Total'])

print(AuroraPlus.KilowattHourUsage['T41'])
print(AuroraPlus.KilowattHourUsage['T31'])
print(AuroraPlus.KilowattHourUsage['Total'])