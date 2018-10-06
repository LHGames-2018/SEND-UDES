class Player:
    def __init__(self, health, maxHealth, carriedResources, carryingCapacity,
                 collectingSpeed, totalResources, attackPower, defence, position, houseLocation,
                 carriedItems, score, name, upgradeLevels):
        self.Health = health
        self.MaxHealth = maxHealth
        self.CarriedResources = carriedResources
        self.CarryingCapacity = carryingCapacity
        self.CollectingSpeed = collectingSpeed
        self.TotalResources = totalResources
        self.AttackPower = attackPower
        self.Defence = defence
        self.Position = position
        self.HouseLocation = houseLocation
        self.CarriedItems = carriedItems
        self.Score = score
        self.Name = name
        self.UpgradeLevels = upgradeLevels

    def getUpgradeLevel(self, type):
        return self.UpgradeLevels[type]
