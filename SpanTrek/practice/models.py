from django.db import models

class DailyChallenge(models.Model):
    """CODES:\n
        CxL - Complete x lessons\n
        Px  - Practice x times\n
        RPx - Do random practice x times\n
        VPx - Do vocabulary practice x times\n
        SPx - Do sentence practice x times\n
        LPx - Do listening practice x times\n
        NWx - Learn x new words\n
        NSx - Learn x new sentences\n
        NAx - Learn x new audio clips\n
        EXx - Earn x experience points\n
    """
    code = models.CharField(max_length=255)
    description = models.TextField()
    max_progress = models.IntegerField(default=1)

    def __str__(self):
        return self.code
