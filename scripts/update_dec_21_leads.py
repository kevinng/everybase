from relationships import models

def run():
    ls = models.Lead.objects.all()
    for l in ls:
        # Copy headline from title
        l.headline = l.title[:80]

        # Generate agent_job from lead_type
        if l.lead_type == 'buying':
            l.agent_job = 'I need an agent to help me buy or source.'
            l.question_2 = 'Do you know any potential buyers?'
        elif l.lead_type == 'selling':
            l.agent_job = 'I need an agent to help me sell or promote.'
            l.question_2 = 'Do you know any potential sellers?'

        l.question_1 = 'Have you dealt with this or similar goods or services before?'
        l.save() # Will refresh slug