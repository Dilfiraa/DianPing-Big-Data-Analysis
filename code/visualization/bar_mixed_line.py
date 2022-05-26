### creat bar mix line
import pyecharts.options as opts
from pyecharts.charts import Bar, Line
from pyecharts.faker import Faker
import pandas as pd

path = 'all.csv'
df = pd.read_csv(path)


df['shop_name'].value_counts()
df_new = df.groupby('shop_name').mean()['shop_star'].to_frame()
df_new['shop_num'] = df.groupby('shop_name').count()['shop_star'].tolist()
df_new = df_new.sort_values(by='shop_num', ascending = False)
df_new['shop_star'] = df_new['shop_star'].map(lambda x:round(x, 2))
df_new = df_new.drop(df_new[(df_new.shop_num < 30)].index)


shop_name = df_new.index.tolist()
shop_num = df_new['shop_num'].tolist()
shop_star = df_new['shop_star'].tolist()

bar = (
    Bar(init_opts=opts.InitOpts(width="1680px", height="800px"))
    .add_xaxis(xaxis_data=shop_name)
    .add_yaxis(
        series_name="店铺数量",
        y_axis=shop_num,
        yaxis_index=1,
    )
    .extend_axis(
        yaxis=opts.AxisOpts(
            name="店铺数量",
            type_="value",
            min_=0,
            max_=220,
            position="left",

        )
    )
    .extend_axis(
        yaxis=opts.AxisOpts(
            type_="value",
            name="店铺评分",
            min_=0,
            max_=5.0,
            position="right",
            splitline_opts=opts.SplitLineOpts(
                is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)
            ),
        )
    )
    .set_global_opts(
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-90)),
        title_opts=opts.TitleOpts(title=""),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
    )
)

line = (
    Line()
    .add_xaxis(xaxis_data=shop_name)
    .add_yaxis(
        series_name="店铺评分", y_axis=shop_star, yaxis_index=2
    )
)

bar.overlap(line).render("bar_mixed_line.html")