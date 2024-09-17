from collections import defaultdict
from datetime import datetime

class ReportGenerator:
    def __init__(self):
        self.task_history = []

    def add_task(self, task_type, query, result, cost, duration):
        self.task_history.append({
            'timestamp': datetime.now(),
            'task_type': task_type,
            'query': query,
            'result': result,
            'cost': cost,
            'duration': duration
        })

    def generate_report(self, time_period='day'):
        report = {
            'total_tasks': len(self.task_history),
            'task_types': defaultdict(int),
            'total_cost': 0,
            'average_duration': 0,
            'most_expensive_task': None,
            'longest_task': None
        }

        for task in self.task_history:
            report['task_types'][task['task_type']] += 1
            report['total_cost'] += task['cost']
            report['average_duration'] += task['duration']

            if not report['most_expensive_task'] or task['cost'] > report['most_expensive_task']['cost']:
                report['most_expensive_task'] = task

            if not report['longest_task'] or task['duration'] > report['longest_task']['duration']:
                report['longest_task'] = task

        if self.task_history:
            report['average_duration'] /= len(self.task_history)

        return report

    def get_task_history(self):
        return self.task_history

report_generator = ReportGenerator()