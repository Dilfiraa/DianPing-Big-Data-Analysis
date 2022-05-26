### creat Treemap
from pyecharts import options as opts
from pyecharts.charts import TreeMap
from pyecharts.globals import ThemeType
import pandas as pd

path = 'all.csv'
df = pd.read_csv(path)

category_name = df['shop_category'].value_counts().index.tolist()
category_num = df['shop_category'].value_counts().tolist()

treemap_list = []
for i in range(len(category_name)):
  treemap_list.append({'value': category_num[i], 'name': category_name[i]})


bar = (
    TreeMap(init_opts=opts.InitOpts(theme=ThemeType.MACARONS, width="1200px", height="600px"))
    .add("菜品", treemap_list,
         levels=[
            opts.TreeMapLevelsOpts(
                treemap_itemstyle_opts=opts.TreeMapItemStyleOpts(
                    border_color="#555", border_width=2, gap_width=2
                )
            )
          ],
    )
    .set_series_opts(label_opts=opts.LabelOpts(position='insideTopLeft'))
    .set_global_opts(title_opts=opts.TitleOpts(title="菜品分布"))
    .render("treemap.html")
)
