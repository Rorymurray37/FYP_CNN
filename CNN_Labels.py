def create_labels(df,col_name, window_size=15):


        row_counter = 0
        total_rows = len(df)
        df["Label"] = 0 #create label col
        Labelcol = df.columns.get_loc('Label')

        print("Calculating labels")


        while row_counter < total_rows:
            if row_counter >= window_size - 1:
                window_begin = row_counter - (window_size - 1)
                window_end = row_counter
                window_middle = (window_begin + window_end) / 2
                window_middle = int(window_middle)


                Min = 10000
                min_index = 0
                Max = 0
                max_index = 0

                for i in range(window_begin, window_end + 1):
                    price = df.iloc[i][col_name]
                    if price < Min:
                        Min = price
                        min_index = i
                    if price > Max:
                        Max = price
                        max_index = i


                if min_index == window_middle:
                    df.iloc[window_middle,Labelcol] = 1
                else:
                    df.iloc[window_middle,Labelcol] = 0

            row_counter = row_counter + 1


def trend_labels(df, col_name, window_size=11, threshold = 3):

        row_counter = 0
        total_rows = len(df)
        df["Label"] = 0 #create label col
        Labelcol = df.columns.get_loc('Label')

        print("trend labels")


        while row_counter < total_rows:
            if row_counter >= window_size - 1:
                window_begin = row_counter - (window_size - 1)
                window_end = row_counter
                window_middle = (window_begin + window_end) / 2

                Min = 10000
                min_index = 0
                Max = 0
                max_index = 0

                for i in range(window_begin, window_end + 1):
                    price = df.iloc[i][col_name]
                    if price < Min:
                        Min = price    #find min
                        min_index = i
                    if price > Max:
                        Max = price    #find max
                        max_index = i

                if(min_index +98 < len(df)):
                    #98 is a week forward
                    diff = df.iloc[min_index+98][col_name] - df.iloc[min_index][col_name]
                    change = diff / df.iloc[min_index][col_name] * 100

                    if(change > threshold):
                        df.iloc[min_index,Labelcol] = 1  #buy
                    else:
                        df.iloc[min_index,Labelcol] = 0  #hold

                        #elif(decrease < threshold * -1):
                        #df.at[min_index,'Label'] = 0  #short




            row_counter = row_counter + 1


def Min_label(df,col_name, window_size=41):


        row_counter = 0
        total_rows = len(df)
        df["Label"] = 0 #create label col
        Labelcol = df.columns.get_loc('Label')

        print("Calculating labels")


        while row_counter < total_rows:
            if row_counter >= window_size - 1:
                window_begin = row_counter - (window_size - 1)
                window_end = row_counter
                window_middle = (window_begin + window_end) / 2
                window_middle = int(window_middle)


                Min = 10000
                min_index = 0
                Max = 0
                max_index = 0

                for i in range(window_begin, window_end + 1):
                    price = df.iloc[i][col_name]
                    if price < Min:
                        Min = price
                        min_index = i
                    if price > Max:
                        Max = price
                        max_index = i


                diff = df.iloc[window_end][col_name] - df.iloc[min_index][col_name]
                change = diff / df.iloc[min_index][col_name] * 100


                if min_index == window_middle and change > 2:
                    df.iloc[window_middle,Labelcol] = 1
                else:
                    df.iloc[window_middle,Labelcol] = 0

            row_counter = row_counter + 1
            
            
            
def bullish_label(df,col_name, window_size=15):


        row_counter = 0
        total_rows = len(df)
        df["Label"] = 0 #create label col
        Labelcol = df.columns.get_loc('Label')

        print("Calculating bullish labels")


        while row_counter < total_rows:
            if row_counter >= window_size - 1:
                window_begin = row_counter - (window_size - 1)
                window_end = row_counter
                window_middle = (window_begin + window_end) / 2
                window_middle = int(window_middle)


                Min = 10000
                min_index = 0
                Max = 0
                max_index = 0

                for i in range(window_begin, window_end + 1):
                    price = df.iloc[i][col_name]
                    if price < Min:
                        Min = price
                        min_index = i
                    if price > Max:
                        Max = price
                        max_index = i


                if min_index == window_begin and max_index == window_end:
                    df.iloc[window_middle,Labelcol] = 1
                else:
                    df.iloc[window_middle,Labelcol] = 0

            row_counter = row_counter + 1            
