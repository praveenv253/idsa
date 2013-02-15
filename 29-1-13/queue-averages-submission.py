"""
Program to simulate a queue and measure average queue length and waiting times
as a function of the arrival time and service time parameters.
This program assumes that both addition to the queue and removal from the queue
follow a Poisson process, meaning that inter-arrival times and individual
service times are exponentially distributed.

Input parameters are the mean arrival rate and the average service time.
"""

import sys

from random import expovariate as expdistr


class Queue(object):
    """Simple implementation of a queue data type."""

    def __init__(self):
        self._queue = []

    def enqueue(self, item):
        """Add an item to the queue. No return value."""
        self._queue.append(item)

    def dequeue(self):
        """Remove the item at the head of the queue. Returns the item."""
        item = self._queue[0]
        self._queue = self._queue[1:]
        return item

    def head(self):
        """
        Return the item at the head of the queue without removal.
        Returns None if the queue is empty.
        """
        try:
            return self._queue[0]
        except IndexError:
            return None

    def update_head(self, attr, value):
        """
        Allows external updating of an attribute of the item at the head of the
        queue.
        Returns nothing.
        """
        setattr(self._queue[0], attr, value)
    
    def is_empty(self):
        """Returns whether or not the queue is empty."""
        return len(self._queue) == 0

    def __len__(self):
        """Return number of items in the queue."""
        return len(self._queue)

    def __repr__(self):
        """String representation of the queue."""
        return str(self._queue)


class Event(object):
    """
    Class to describe an event.
    
    Attributes include:
    - inter-arrival time
    - service time
    """
    
    def __init__(self, *args):
        if args[0] is False:
            # Externally set inter-arrival time and service time
            self.inter_arrival_time = args[1]
            self.service_time = args[2]
        else:
            # Internally set inter-arrival time and service time.
            # In this case, arguments are the respective parameters for the
            # two exponential distributions.
            self.inter_arrival_time = _inter_arrival_time(args[0])
            self.service_time = _service_time(args[1])
    
    def _inter_arrival_time(self, mar):
        # mar is the mean arrival time
        # Inter-arrival time is exponential, with parameter 1/mar
        return expdistr(1 / float(mar))
    
    def _service_time(self, ast):
        # ast is the average service time
        # Service times are also exponential, with parameter 1/ast
        return expdistr(1 / float(ast))
    
    def __repr__(self):
        return unicode((self.inter_arrival_time, self.service_time))


def events():
    """
    Generator for newly incoming events. Implementation dependent.
    Here, reads a line containing arrival time and service time from the
    event buffer (in case an event has been un-generated), otherwise from
    standard input.
    Returns events generated from successive lines on iteration.
    """
    prev_arrival_time = 0
    for line in sys.stdin.readlines():
        line = line.replace('\n', '').replace('\r', '')
        arrival_time, service_time = line.split()
        arrival_time = float(arrival_time)
        service_time = float(service_time)
        yield Event(False, arrival_time-prev_arrival_time, service_time)
        prev_arrival_time = arrival_time
    
def simulate_queue():
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
    for event in events():
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
            # The head is done, so let's remove it.
            completed_event = q.dequeue()
            # We need to catch the head and ask it how long it waited in the
            # queue
            total_waiting_time += (  completed_event.exit_time
                                   - completed_event.arrival_time
                                   - completed_event.service_time )
            num_events += 1
            # If the queue is now empty, we can simply enqueue the new event
            # without worries. It goes straight to processing. No queue length
            # increase and no waiting time increase.
            l = len(q)
            if l == 0:
                event.exit_time = event.arrival_time + event.service_time
                q.enqueue(event)
                continue
            # If there are other events in the queue, before we enqueue the new
            # event, we need to check whether the new head will finish before
            # this event arrives. If that is the case, waiting times, etc.
            # could change.
            # First, we need to set the new head's exit time
            new_exit_time = t + q.head().service_time
            q.update_head('exit_time', new_exit_time)
            # Then, check whether this exit time is before the arrival time of
            # the latest event.
            while(q.head().exit_time <= event.arrival_time):
                # In order to update the total_length_time, we note that the
                # events still in the queue need to wait until the new head
                # completes. So, each waiting queue member adds one queue
                # length until then. At this stage, len(q) >= 1.
                # There are potentially another (l-1) events that were already
                # in the queue. These add one queue length *each* until the new
                # head's exit time.
                total_length_time += (l - 1) * (new_exit_time - t)
                # Catch the event as it comes out of the queue in order to find
                # out how long it waited in the queue.
                completed_event = q.dequeue()
                total_waiting_time += (  completed_event.exit_time
                                       - completed_event.arrival_time
                                       - completed_event.service_time )
                num_events += 1
                t = new_exit_time
                l = len(q)
                if l == 0:
                    break
                new_exit_time = t + q.head().service_time
                q.update_head('exit_time', new_exit_time)

            # t is not new_exit_time yet! new_exit_time here corresponds to the
            # exit time of the current head, which is now strictly greater than
            # the newest event's arrival time.

            # We can finally add the latest event.
            q.enqueue(event)
            # If the head is the newly added event, then we need to consider
            # time it takes since *its* arrival. Otherwise, we consider the
            # time taken since the previous event exited.
            l = len(q)
            if l == 1:
                new_exit_time = event.arrival_time + event.service_time
            else:
                # Otherwise, we already have our exit time - which is the exit
                # time of the newest head in the queue.
                pass
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
    aql, awt = simulate_queue()
    print '%.4f' % aql
    print '%.4f' % awt

