from .models import Promise, Slot

def flatten_promises(starting_datetime, ending_datetime):
    promise_list = list(Promise.objects.filter(start__gte=starting_datetime, stop__lte=ending_datetime).order_by("start"))
    flat_list = []

    while(len(promise_list) > 0):
        concurrent_promises = []

        earliest_promise = promise_list.pop(0)

        for poss_conc_promise in promise_list:
            if poss_conc_promise.start <= earliest_promise.stop:
                concurrent_promises.append(poss_conc_promise)
                promise_list.remove(poss_conc_promise)

        if len(concurrent_promises) > 0:
            final_endtime = max(max([promise.stop for promise in concurrent_promises]),earliest_promise.stop)
        else:
            final_endtime = earliest_promise.stop

        flat_list.append((earliest_promise.start, final_endtime))

    return flat_list


def compare_slots_and_promises(starting_datetime, ending_datetime):
    slot_list = list(Slot.objects.filter(start__gte=starting_datetime, stop__lte=ending_datetime).order_by("start"))
    flattened_promises = flatten_promises(starting_datetime, ending_datetime)

    list_of_problems = []
    for slot in slot_list:
        relevant_promise_list_index = 0
        while relevant_promise_list_index < len(flattened_promises) and flattened_promises[relevant_promise_list_index][1] < slot.start:
            relevant_promise_list_index += 1

        if relevant_promise_list_index == len(flattened_promises):
            # Slot happens after all promises
            list_of_problems.append((slot.start, slot.stop))
        else:
            current_time = slot.start
            problems = []

            while current_time != slot.stop:
                #Slot's endtime is after all promises
                if relevant_promise_list_index == len(flattened_promises):
                    problems.append((current_time, slot.stop))
                    break

                #promise starts before or right at the slot
                if flattened_promises[relevant_promise_list_index][0] <= current_time:
                    current_time = min(flattened_promises[relevant_promise_list_index][1], slot.stop)
                    relevant_promise_list_index += 1

                #same between slot start and the promise start
                elif flattened_promises[relevant_promise_list_index][0] >= current_time:
                    new_time = min(slot.stop, flattened_promises[relevant_promise_list_index][0])
                    problems.append((current_time, new_time))
                    current_time = new_time

            list_of_problems += problems

    return list_of_problems