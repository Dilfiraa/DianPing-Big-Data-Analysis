import * as echarts from 'echarts';

var chartDom = document.getElementById('main');
var myChart = echarts.init(chartDom);
var option;

const data = [
  [
    [1237, 3.82, 851.8, '东丽区'],
    [937, 3.84, 885.68, '北辰区'],
    [2301, 4.23, 544.22, '南开区'],
    [2060, 4.21, 720.37, '和平区'],
    [50, 3.81, 501.72, '宁河区'],
    [133, 3.69, 564.73, '宝坻区'],
    [627, 3.72, 950.73, '武清区'],
    [2349, 4.12, 280.1, '河东区'],
    [1271, 3.97, 383.69, '河北区'],
    [1787, 4.1, 708.82, '河西区'],
    [894, 3.81, 710.01, '津南区'],
    [2161, 3.91, 5760.15, '滨海新区'],
    [1352, 4.0, 174.89, '红桥区'],
    [289, 3.73, 350.91, '蓟州区'],
    [1411, 3.92, 964.71, '西青区'],
    [268, 3.73, 583.38, '静海区']
  ]
];
option = {
  title: {
    text: '各区的店铺数量和店铺评分及GDP之间的关系',
    left: '5%',
    top: '3%'
  },
  tooltip: {
    padding: 5,
    borderWidth: 1,
    formatter: function (param) {
      var value = param.value;
      // prettier-ignore
      return value[3] + '<br>' +
           '店铺数量：' + value[0] + '<br>' +
           '店铺平均评分：' + value[1] + '<br>' + 
           '区域GDP：' + value[2] + '<br>';
    }
  },
  legend: {
    right: '10%',
    top: '3%',
    data: ['1990', '2015']
  },
  grid: {
    left: '8%',
    top: '10%'
  },
  xAxis: {
    splitLine: {
      lineStyle: {
        type: 'dashed'
      }
    }
  },
  yAxis: {
    splitLine: {
      lineStyle: {
        type: 'dashed'
      }
    },
    scale: true
  },
  series: [
    {
      name: '',
      data: data[0],
      type: 'scatter',
      symbolSize: function (data) {
        return Math.sqrt(data[2]);
      },
      itemStyle: {
        shadowBlur: 10,
        shadowColor: 'rgba(120, 36, 50, 0.5)',
        shadowOffsetY: 5,
        color: new echarts.graphic.RadialGradient(0.4, 0.3, 1, [
          {
            offset: 0,
            color: 'rgb(251, 118, 123)'
          },
          {
            offset: 1,
            color: 'rgb(204, 46, 72)'
          }
        ])
      }
    }
  ]
};

option && myChart.setOption(option);
