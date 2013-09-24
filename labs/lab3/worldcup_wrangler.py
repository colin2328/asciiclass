from wrangler import dw
import sys

if(len(sys.argv) < 3):
	sys.exit('Error: Please include an input and output file.  Example python script.py input.csv output.csv')

w = dw.DataWrangler()

# Split data repeatedly on newline  into  rows
w.add(dw.Split(column=["data"],
               table=0,
               status="active",
               drop=True,
               result="row",
               update=False,
               insert_position="right",
               row=None,
               on="\n",
               before=None,
               after=None,
               ignore_between=None,
               which=1,
               max=0,
               positions=None,
               quote_character=None))

# Cut  on '"'
w.add(dw.Cut(column=[],
             table=0,
             status="active",
             drop=False,
             result="column",
             update=True,
             insert_position="right",
             row=None,
             on="\"",
             before=None,
             after=None,
             ignore_between=None,
             which=1,
             max=0,
             positions=None))

# Cut from data between ']]' and ', '
w.add(dw.Cut(column=["data"],
             table=0,
             status="active",
             drop=False,
             result="column",
             update=True,
             insert_position="right",
             row=None,
             on=".*",
             before=", ",
             after="]]",
             ignore_between=None,
             which=1,
             max=1,
             positions=None))

# Cut from data before '{'
w.add(dw.Cut(column=["data"],
             table=0,
             status="active",
             drop=False,
             result="column",
             update=True,
             insert_position="right",
             row=None,
             on=".*",
             before="{",
             after=None,
             ignore_between=None,
             which=1,
             max=1,
             positions=None))

# Cut from data before '(\[\['
w.add(dw.Cut(column=["data"],
             table=0,
             status="active",
             drop=False,
             result="column",
             update=True,
             insert_position="right",
             row=None,
             on=".*",
             before="\\(\\[\\[",
             after=None,
             ignore_between=None,
             which=1,
             max=1,
             positions=None))

# Cut from data on '[\[ any number  FIFA  any word   any word \|'
w.add(dw.Cut(column=["data"],
             table=0,
             status="active",
             drop=False,
             result="column",
             update=True,
             insert_position="right",
             row=None,
             on="\\[\\[[0-9]+ FIFA [a-zA-Z]+ [a-zA-Z]+\\|",
             before=None,
             after=None,
             ignore_between=None,
             which=1,
             max="0",
             positions=None))

# Cut from data on ']]'
w.add(dw.Cut(column=["data"],
             table=0,
             status="active",
             drop=False,
             result="column",
             update=True,
             insert_position="right",
             row=None,
             on="]]",
             before=None,
             after=None,
             ignore_between=None,
             which=1,
             max="0",
             positions=None))

# Cut from data between '1990' and ')'
w.add(dw.Cut(column=["data"],
             table=0,
             status="active",
             drop=False,
             result="column",
             update=True,
             insert_position="right",
             row=None,
             on=".*",
             before="\\)",
             after="1990",
             ignore_between=None,
             which=1,
             max=1,
             positions=None))

# Cut from data after '}}'
w.add(dw.Cut(column=["data"],
             table=0,
             status="active",
             drop=False,
             result="column",
             update=True,
             insert_position="right",
             row=None,
             on=".*",
             before=None,
             after="}}",
             ignore_between=None,
             which=1,
             max=1,
             positions=None))

# Cut from data between '1974' and ','
w.add(dw.Cut(column=["data"],
             table=0,
             status="active",
             drop=False,
             result="column",
             update=True,
             insert_position="right",
             row=None,
             on=".*",
             before=",",
             after="1974",
             ignore_between=None,
             which=1,
             max=1,
             positions=None))

# Cut from data on '{{ any word |'
w.add(dw.Cut(column=["data"],
             table=0,
             status="active",
             drop=False,
             result="column",
             update=True,
             insert_position="right",
             row=None,
             on="{{[a-zA-Z]+\\|",
             before=None,
             after=None,
             ignore_between=None,
             which=1,
             max=1,
             positions=None))

# Cut from data on '}}'
w.add(dw.Cut(column=["data"],
             table=0,
             status="active",
             drop=False,
             result="column",
             update=True,
             insert_position="right",
             row=None,
             on="}}",
             before=None,
             after=None,
             ignore_between=None,
             which=1,
             max=1,
             positions=None))

# Delete  rows where data = '|-'
w.add(dw.Filter(column=[],
                table=0,
                status="active",
                drop=False,
                row=dw.Row(column=[],
             table=0,
             status="active",
             drop=False,
             conditions=[dw.Eq(column=[],
            table=0,
            status="active",
            drop=False,
            lcol="data",
            value="|-",
            op_str="=")])))

# Cut from data on '| any number '
w.add(dw.Cut(column=["data"],
             table=0,
             status="active",
             drop=False,
             result="column",
             update=True,
             insert_position="right",
             row=None,
             on="\\|\\d+",
             before=None,
             after=None,
             ignore_between=None,
             which=1,
             max=1,
             positions=None))

# Delete  rows where data = '|align=center| —'
w.add(dw.Filter(column=[],
                table=0,
                status="active",
                drop=False,
                row=dw.Row(column=[],
             table=0,
             status="active",
             drop=False,
             conditions=[dw.Eq(column=[],
            table=0,
            status="active",
            drop=False,
            lcol="data",
            value="|align=center| —",
            op_str="=")])))

# Cut from data on '('
w.add(dw.Cut(column=["data"],
             table=0,
             status="active",
             drop=False,
             result="column",
             update=True,
             insert_position="right",
             row=None,
             on="\\(",
             before=None,
             after=None,
             ignore_between=None,
             which=1,
             max=1,
             positions=None))

# Cut from data on ')'
w.add(dw.Cut(column=["data"],
             table=0,
             status="active",
             drop=False,
             result="column",
             update=True,
             insert_position="right",
             row=None,
             on="\\)",
             before=None,
             after=None,
             ignore_between=None,
             which=1,
             max=1,
             positions=None))

# Delete row 94
w.add(dw.Filter(column=[],
                table=0,
                status="active",
                drop=False,
                row=dw.Row(column=[],
             table=0,
             status="active",
             drop=False,
             conditions=[dw.RowIndex(column=[],
                  table=0,
                  status="active",
                  drop=False,
                  indices=[93])])))

# Delete row 94
w.add(dw.Filter(column=[],
                table=0,
                status="active",
                drop=False,
                row=dw.Row(column=[],
             table=0,
             status="active",
             drop=False,
             conditions=[dw.RowIndex(column=[],
                  table=0,
                  status="active",
                  drop=False,
                  indices=[93])])))

# Delete row 94
w.add(dw.Filter(column=[],
                table=0,
                status="active",
                drop=False,
                row=dw.Row(column=[],
             table=0,
             status="active",
             drop=False,
             conditions=[dw.RowIndex(column=[],
                  table=0,
                  status="active",
                  drop=False,
                  indices=[93])])))

# Cut from data on '[\[#1\|\*'
w.add(dw.Cut(column=["data"],
             table=0,
             status="active",
             drop=False,
             result="column",
             update=True,
             insert_position="right",
             row=None,
             on="\\[\\[#1\\|\\*",
             before=None,
             after=None,
             ignore_between=None,
             which=1,
             max=1,
             positions=None))

# Cut from data on '! Team !! Titles !! Runners-up !! Third place !! Fourth place !! Top 4 <br/> finishes'
w.add(dw.Cut(column=["data"],
             table=0,
             status="active",
             drop=False,
             result="column",
             update=True,
             insert_position="right",
             row=None,
             on="! Team !! Titles !! Runners-up !! Third place !! Fourth place !! Top 4 <br/> finishes",
             before=None,
             after=None,
             ignore_between=None,
             which=1,
             max="0",
             positions=None))

# Wrap empty rows
w.add(dw.Wrap(column=[],
              table=0,
              status="active",
              drop=False,
              row=dw.Row(column=[],
             table=0,
             status="active",
             drop=False,
             conditions=[dw.Empty(column=[],
               table=0,
               status="active",
               drop=False,
               percent_valid=0,
               num_valid=0)])))

# Fold wrap, wrap1, wrap2, wrap3...  using  header as a key
w.add(dw.Fold(column=["wrap","wrap1","wrap2","wrap3","wrap4","wrap5"],
              table=0,
              status="active",
              drop=False,
              keys=[-1]))

# Translate value up
w.add(dw.Translate(column=["value"],
                   table=0,
                   status="active",
                   drop=False,
                   direction="up",
                   values=1))

# Drop value
w.add(dw.Drop(column=["value"],
              table=0,
              status="active",
              drop=True))

# Extract from fold between positions 4, 5
w.add(dw.Extract(column=["fold"],
                 table=0,
                 status="active",
                 drop=False,
                 result="column",
                 update=False,
                 insert_position="right",
                 row=None,
                 on=None,
                 before=None,
                 after=None,
                 ignore_between=None,
                 which=1,
                 max=1,
                 positions=[4,5]))

# Drop fold
w.add(dw.Drop(column=["fold"],
              table=0,
              status="active",
              drop=True))

# Extract from translate on ' any word '
w.add(dw.Extract(column=["translate"],
                 table=0,
                 status="active",
                 drop=False,
                 result="column",
                 update=False,
                 insert_position="right",
                 row=None,
                 on="[a-zA-Z]+",
                 before=None,
                 after=None,
                 ignore_between=None,
                 which=1,
                 max=1,
                 positions=None))

# Fill extract1  with values from above
w.add(dw.Fill(column=["extract1"],
              table=0,
              status="active",
              drop=False,
              direction="down",
              method="copy",
              row=None))

# Delete  rows where extract is null
w.add(dw.Filter(column=[],
                table=0,
                status="active",
                drop=False,
                row=dw.Row(column=[],
             table=0,
             status="active",
             drop=False,
             conditions=[dw.IsNull(column=[],
                table=0,
                status="active",
                drop=False,
                lcol="extract",
                value=None,
                op_str="is null")])))

# Delete  rows where extract = '5'
w.add(dw.Filter(column=[],
                table=0,
                status="active",
                drop=False,
                row=dw.Row(column=[],
             table=0,
             status="active",
             drop=False,
             conditions=[dw.Eq(column=[],
            table=0,
            status="active",
            drop=False,
            lcol="extract",
            value="5",
            op_str="=")])))

# Split translate repeatedly on ','  into  rows
w.add(dw.Split(column=["translate"],
               table=0,
               status="active",
               drop=True,
               result="row",
               update=False,
               insert_position="right",
               row=None,
               on=",",
               before=None,
               after=None,
               ignore_between=None,
               which=1,
               max="0",
               positions=None,
               quote_character=None))

# Cut from translate on '*'
w.add(dw.Cut(column=["translate"],
             table=0,
             status="active",
             drop=False,
             result="column",
             update=True,
             insert_position="right",
             row=None,
             on="\\*",
             before=None,
             after=None,
             ignore_between=None,
             which=1,
             max=1,
             positions=None))

# Delete row 77
w.add(dw.Filter(column=[],
                table=0,
                status="active",
                drop=False,
                row=dw.Row(column=[],
             table=0,
             status="active",
             drop=False,
             conditions=[dw.RowIndex(column=[],
                  table=0,
                  status="active",
                  drop=False,
                  indices=[76])])))

w.apply_to_file(sys.argv[1]).print_csv(sys.argv[2])