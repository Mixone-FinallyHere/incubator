from .models import Promise, Slot

def flatten_promises(starting_datetime, ending_datetime):
    promise_list = list(Promise.objects.filter(start__gte=starting_datetime, stop__lte=ending_datetime).order_by("start"))
    flat_list = []

    for elem in promise_list:
        print(elem.start.time(), "until", elem.stop.time())


    while(len(promise_list) > 0):
        concurrent_promises = []

        earliest_promise = promise_list.pop(0)
        start_time = earliest_promise.start

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