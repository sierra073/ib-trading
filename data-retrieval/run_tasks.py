# To be run with docker exec
def get_earliest_date(client, contract):
    return client.reqHeadTimeStamp(4101, contract, 'TRADES', 0, 1)


    # d = datetime.now()
    # earliest_date = datetime.strptime(get_earliest_date(client, contract), "%Y%m%d %H:%M:%S")
    # delta = d - earliest_date
    # number_of_days = delta.days
    # print('number_of_days: ', number_of_days)

    # for i in range(number_of_days):
        # d = d - timedelta(days=1)
