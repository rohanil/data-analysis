$(document).ready(function () {
                  $(chartID2).highcharts({
                                         chart: {
                                         type: 'spline'
                                         },
                                         title: {
                                         text: 'Accounts Trend'
                                         },
                                         subtitle: {
                                         text: 'Top 10 Customers'
                                         },
                                         xAxis: {
                                         type: 'datetime',
                                         dateTimeLabelFormats: { // don't display the dummy year
                                         month: '%e. %b',
                                         year: '%b'
                                         },
                                         title: {
                                         text: 'Date'
                                         }
                                         },
                                         yAxis: {
                                         title: {
                                         text: 'Accounts'
                                         },
                                         min: 0
                                         },
                                         tooltip: {
                                         shared: false,
                                         valueSuffix: ' Accounts'
                                         },
                                         
                                         series: series2
                                         });
                  });