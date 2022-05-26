### creat wordcloud
from pyecharts.charts.basic_charts.wordcloud import WordCloud
from pyecharts.charts import Bar
from pyecharts import options as opts
import pandas as pd

path = 'all.csv'
df = pd.read_csv(path)

shop_name = df['shop_name'].value_counts().index.tolist()
shop_num = df['shop_name'].value_counts().tolist()

Wordcloud_list = []
for i in range(len(shop_name)):
  if shop_num[i] < 20:
    break
  else:
    Wordcloud_list.append((shop_name[i], shop_num[i]))

wordcloud = (
    WordCloud(init_opts=opts.InitOpts(theme='infographic', width="1200px", height="600px"))
    .add(series_name="连锁店铺分布", data_pair=Wordcloud_list, word_size_range=[6, 66], rotate_step=90)
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="连锁店铺分布", title_textstyle_opts=opts.TextStyleOpts(font_size=23)
        ),
        tooltip_opts=opts.TooltipOpts(is_show=True),
        toolbox_opts=opts.ToolboxOpts(),
    )
    .render('wordcloud.html')
)