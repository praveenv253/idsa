#!/usr/bin/env python

"""
Program to simulate a queue and measure average queue length and waiting times
as a function of the arrival time and service time parameters.
This program assumes that both addition to the queue and removal from the queue
follow a Poisson process, meaning that inter-arrival times and individual
service times are exponentially distributed.

Input parameters are the mean arrival rate and the average service time.
"""

import sys

from queue import Queue
from event import Event

if len(sys.argv) != 4:
    print 'Insufficient number of command line parameters.'
    print ('Usage: %s <mean_arrival_rate> <average_service_time> <max_events>'
           % sys.argv[0])
    sys.exit(1)

try:
    mean_arrival_rate = float(sys.argv[1])
    average_service_time = float(sys.argv[2])
except ValueError:
    print 'Input parameters must be parseable as floating point numbers'
    sys.exit(1)

def events(mar, ast):
    """
    Generator for incoming events. Implementation dependent.
    Currently creates a new event each time it is called, until the global
    variable MAXEVENTS is exceeded.
    """
    #num_events = 0
    #while num_events < MAXEVENTS:
    #    yield Event(mar, ast)
    #    num_events += 1
    for e in [ Event(False, 0.0, 1.0),
               Event(False, 1.2, 1.0),
               Event(False, 0.8, 0.8),
               Event(False, 0.1, 0.6),
             ]:
        yield e

def simulate_queue(mar, ast):
    """
    Function to iterate through events and perform the main queue simulation.
    
    Parameters: mean arrival time and average service time.
    Returns: mean queue length and mean waiting time per customer.
    """

    # Initialize the queue
    q = Queue()

    # This variable stores the arrival time of the last event to enter the
    # queue. This is required because only the inter-arrival times of events
    # are known, not their absolute arrival times.
    last_arrival_time = 0.0

    # Global time parameter. This will usually point to the exit time of the
    # item that is currently at the head of the queue.
    t = 0.0

    # Variables to record waiting times and queue length
    num_events = 0
    total_waiting_time = 0.0
    total_length_time = 0.0

    # Start iterating through events
    for event in events(mar, ast):
        print t
        # Figure out the new event's absolute arrival time...
        event.arrival_time = last_arrival_time + event.inter_arrival_time
        # ...and update last_arrival_time to match this event
        last_arrival_time = event.arrival_time
        
        # We'll need to compare the arrival time of the new event with the exit
        # time of the event at the head of the queue
        head = q.head()
        if head is None:
            # If the queue is empty, just add the new event.
            event.exit_time = event.arrival_time + event.service_time
            q.enqueue(event)
            # No one else can get serviced while this event is at the counter.
            # Let's skip to when this event exits.
            t = event.exit_time
            continue
        if head.exit_time > event.arrival_time:
            # We're now at the head's exit time, but this new event came in
            # before the head could finish. So the new event gets queued.
            q.enqueue(event)
            # This event must now wait in the queue until the head exits. This
            # means that it adds one to the queue length until then. We'll take
            # care of queue lengths after then later.
            total_length_time += 1 * (head.exit_time - event.arrival_time)
            # We can't do anything more. Let's check if another event happened
            # to come in before the head could finish.
            continue
        if head.exit_time <= event.arrival_time:
            # This event actually arrived just when or after the head finished.
            # Let's queue the new event for now.
            q.enqueue(event)
            # The head is done, so let's remove it.
            completed_event = q.dequeue()
            # We need to catch the head and ask it how long it waited in the
            # queue
            total_waiting_time += (  completed_event.exit_time
                                   - completed_event.arrival_time
                                   - completed_event.service_time )
            num_events += 1
            # Before we enqueue the new event, we need to check whether 
            # We now need to set the new head's exit time - note that the
            # presence of a new head is guaranteed, since we just added a new
            # event.
            # If the head is the newly added event, then we need to consider
            # time it takes since *its* arrival. Otherwise, we consider the
            # time taken since the previous event exited.
            l = len(q)
            if l == 1:
                new_exit_time = event.arrival_time + event.service_time
            else:
                new_exit_time = t + q.head().service_time
            q.update_head('exit_time', new_exit_time)
            # In order to update the total_length_time, we note that the events
            # still in the queue need to wait until the new head completes. So,
            # each waiting queue member adds one queue length until then.
            # Note: l must be at least 1, since a new event was added.
            if l == 1:
                # l is 1, meaning that the new event immediately became the
                # head. Hence, it does not contribute to the queue length.
                pass
            else:
                # l is greater than or equal to 2. Now, there is a new event
                # which contributes one queue length, starting from its time
                # of arrival, until the new head's exit time.
                total_length_time += 1 * (new_exit_time - event.arrival_time)
                # Additionally, there are potentially another (l-2) events that
                # were already in the queue. These add one queue length *each*
                # until the new head's exit time.
                total_length_time += (l - 2) * (new_exit_time - t)
            # Once again, no one can get serviced until the new head leaves. So
            # it's safe to jump forward in time.
            t = new_exit_time
    
    # Now to remove elements that are still left in the queue
    # Note that there will always be at least one event left in the queue
    completed_event = q.dequeue()
    total_waiting_time += (  completed_event.exit_time
                           - completed_event.arrival_time
                           - completed_event.service_time )
    num_events += 1
    while len(q) > 0:
        new_exit_time = t + q.head().service_time
        q.update_head('exit_time', new_exit_time)
        # In order to update the total_length_time, we note that the events
        # still in the queue need to wait until the new head completes. So,
        # each waiting queue member adds one queue length until then.
        # Note: l must be at least 1, since a new event was added.
        l = len(q)
        if l > 1:
            # There are potentially another (l-1) events that were already in
            # the queue. These add one queue length *each* until the new head's
            # exit time.
            total_length_time += (l - 1) * (new_exit_time - t)
        # Catch the event as it comes out of the queue in order to find out how
        # long it waited in the queue.
        completed_event = q.dequeue()
        total_waiting_time += (  completed_event.exit_time
                               - completed_event.arrival_time
                               - completed_event.service_time )
        num_events += 1
        t = new_exit_time

    avg_queue_length = total_length_time / t
    avg_waiting_time = total_waiting_time / num_events
    return avg_queue_length, avg_waiting_time

if __name__ == '__main__':
    aql, awt = simulate_queue(mean_arrival_rate, average_service_time)
    print '%.4f' % aql
    print '%.4f' % awt

