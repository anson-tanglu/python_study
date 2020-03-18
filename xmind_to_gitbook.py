import pandas as pd
import re
import sys

pd.set_option('display.max_columns', None)

xmind_md_file = sys.argv[1]

source_file = open(xmind_md_file)

df1 = pd.DataFrame()

cur_level = 0
pre_level = 0
max_level = 0
df1_cnt = 1
df2_cnt = 1
df3_cnt = 1
df4_cnt = 1
line_num = 0

# 10: means max level
pre_level_arr = [0]*10
df_cnt_arr = [1]*10

while True:
    txt = source_file.readline()
    if not txt:
        for i in range(1,pre_level+1):
            df1.loc[df1.line_num == pre_level_arr[i], 'rowspan'] = df_cnt_arr[i]
        break
    line_num = line_num +1
    if re.match("#\s", txt):
        local_temp = txt.split(" ")
        title = local_temp[1]
    elif re.match("##\s", txt):
        new_f1 = txt.split(" ")
        cur_level = 1
        dic = {'line_num': line_num, 'Feature':new_f1[1].strip(), 'rowspan':df_cnt_arr[cur_level], 'depth': cur_level, 'desc': ""}
        df1 = df1.append(dic, ignore_index=True)
        if cur_level <= pre_level:
            df1.loc[df1.line_num == pre_line_num_f1, 'rowspan'] = df_cnt_arr[cur_level]
            for i in range(cur_level+1,pre_level+1):
                df1.loc[df1.line_num == pre_level_arr[i], 'rowspan'] = df_cnt_arr[i]

            for i in range(cur_level,pre_level+1):
                df_cnt_arr[i] = 1

        pre_line_num_f1 = line_num 
        pre_level_arr[cur_level] = pre_line_num_f1

        if cur_level > max_level:
            max_level = cur_level

        pre_level = cur_level
    elif re.match("###\s", txt):
        new_f2 = txt.split(" ")
        cur_level = 2
        dic = {'line_num': line_num, 'Second Feature':new_f2[1].strip(), 'rowspan':df_cnt_arr[cur_level], 'depth':cur_level, 'desc': ""}
        df1 = df1.append(dic, ignore_index=True)
        for i in range(1,cur_level):
            df_cnt_arr[i] = df_cnt_arr[i] +1 

        if cur_level <= pre_level:
            df1.loc[df1.line_num == pre_line_num_f2, 'rowspan'] = df_cnt_arr[cur_level]
            df_cnt_arr[cur_level] = 1
            if cur_level < pre_level:
                df1.loc[df1.line_num == pre_level_arr[pre_level],'rowspan'] = df_cnt_arr[pre_level]

        pre_line_num_f2 = line_num
        pre_level_arr[cur_level] = pre_line_num_f2

        if cur_level > max_level:
            max_level = cur_level

        pre_level = cur_level
    elif re.match("^-\s", txt):
        new_f3 = txt.replace("-"," ")
        cur_level = 3
        dic = {'line_num': line_num, 'Third Feature':new_f3.strip(), 'rowspan':df_cnt_arr[cur_level], 'depth':cur_level, 'desc': ""}
        df1 = df1.append(dic, ignore_index=True)
        for i in range(1,cur_level):
            df_cnt_arr[i] = df_cnt_arr[i] +1 

        if cur_level <= pre_level:
            df1.loc[df1.line_num == pre_line_num_f3, 'rowspan'] = df_cnt_arr[cur_level]
            df_cnt_arr[cur_level] = 1
            if cur_level < pre_level:
                df1.loc[df1.line_num == pre_level_arr[pre_level], 'rowspan'] = df_cnt_arr[pre_level]

        pre_line_num_f3 = line_num
        pre_level_arr[cur_level] = pre_line_num_f3

        if cur_level > max_level:
            max_level = cur_level

        pre_level = cur_level
    elif re.match("^\t-\s", txt):
        new_f4 = txt.replace("\t-"," ")
        cur_level =4
        dic = {'line_num': line_num, 'Fouth Feature':new_f4.strip(), 'rowspan':df_cnt_arr[cur_level], 'depth':cur_level, 'desc': ""}
        df1 = df1.append(dic, ignore_index=True)
        for i in range(1,cur_level):
            df_cnt_arr[i] = df_cnt_arr[i] +1 

        if cur_level <= pre_level:
            df1.loc[df1.line_num == pre_line_num_f4, 'rowspan'] = df_cnt_arr[cur_level]
            df_cnt_arr[cur_level] = 1 
            if cur_level < pre_level:
                df1.loc[df1.line_num == pre_level_arr[pre_level], 'rowspan'] = df_cnt_arr[pre_level]

        pre_line_num_f4 = line_num
        pre_level_arr[cur_level] = pre_line_num_f4

        if cur_level > max_level:
            max_level = cur_level

        pre_level = cur_level
    elif re.match("^\t\t-\s", txt):
        new_f5 = txt.replace("\t\t-"," ")
        cur_level = 5
        dic = {'line_num': line_num, 'Fivth Feature':new_f5.strip(), 'rowspan':df_cnt_arr[cur_level], 'depth':cur_level, 'desc':""}
        df1 = df1.append(dic, ignore_index=True)
        for i in range(1,cur_level):
            df_cnt_arr[i] = df_cnt_arr[i] +1 

        if cur_level <= pre_level:
            df1.loc[df1.line_num == pre_line_num_f5, 'rowspan'] = df_cnt_arr[cur_level]
            df_cnt_arr[cur_level] = 1
            if cur_level < pre_level:
                df1.loc[df1.line_num == pre_level_arr[pre_level], 'rowspan'] = df_cnt_arr[pre_level]

        pre_line_num_f5 = line_num
        pre_level_arr[cur_level] = pre_line_num_f5

        if cur_level > max_level:
            max_level = cur_level

        pre_level = cur_level
    elif re.match("^\w", txt):
        local_temp = txt.strip()
        txt_line_num = pre_level_arr[pre_level]
        df1.loc[df1.line_num == txt_line_num, 'desc'] = local_temp

df1.to_csv('text.csv')
