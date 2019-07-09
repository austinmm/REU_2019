##### Display_Data.py #####

from plotly.offline import init_notebook_mode, iplot, plot
# Creates figures for plotly
import plotly.graph_objs as go
import statistics  # mean(), stdev(), variance()


class Display_Data:

    Configure_Browser_State = False

    @staticmethod
    def configure_plotly_browser_state():
        # Allows use to view the plotly results in colab
        import IPython
        display(IPython.core.display.HTML
            ('''
                <script src="/static/components/requirejs/require.js"></script>
                <script>
                  requirejs.config({
                    paths: {
                      base: '/static/base',
                      plotly: 'https://cdn.plot.ly/plotly-1.5.1.min.js?noext',
                    },
                  });
                </script>
            ''')
        )

    @staticmethod
    def prepare_enviornment():
        if Display_Data.Configure_Browser_State:
            Display_Data.configure_plotly_browser_state()
            init_notebook_mode(connected=False)

    @staticmethod
    def display_results(fig, file_name):
        if Display_Data.Configure_Browser_State:
            iplot(fig, filename=file_name)
        else:
            plot(fig, filename=file_name)

    @staticmethod
    def plotly_create_pie_graph(label, dictionary):
        Display_Data.prepare_enviornment()
        if len(dictionary) == 0:
            return
        values = list(dictionary.values())
        labels = list(dictionary.keys())
        title = "Pie Graph of " + label
        data = {"values": values, "labels": labels,
                "textinfo": "percent", "hoverinfo": "label+value", "hole": .5, "type": "pie"}
        inner_text = str(len(dictionary)) + " Results<br>within Percentile"
        fig = {
            "data": [data],
            "layout": {
                "title": title,
                "annotations": [
                    {
                        "font": {
                            "size": 20
                        },
                        "showarrow": False,
                        "text": inner_text,
                        "x": 0.5,
                        "y": 0.5
                    }
                ]
            }
        }
        Display_Data.display_results(fig, 'pie_graph.html')

    @staticmethod
    def plotly_create_histogram(array, bin_size, x_label, showPercentage):
        Display_Data.prepare_enviornment()
        mu = statistics.mean(array)  # mean of distribution
        sigma = statistics.stdev(array)  # standard deviation of distribution
        title = u'Histogram of ' + x_label + ': \u03BC	= ' + str(round(mu, 2)) + ', \u03C3	 = ' + str(
            round(sigma, 2))
        histnorm = 'percent' if showPercentage else ''
        y_label = 'Probability' if showPercentage else 'Count'
        start = min(array)
        end = max(array)
        #size = int(round((end - start) / num_bins))
        data_layout = go.Histogram(
            x=array,
            histnorm=histnorm,
            name='data',
            #nbinsx=num_bins,
            xbins=dict(start=start, end=end, size=bin_size),
            marker=dict(color='#45b09d'),
            opacity=0.75
        )
        data = [data_layout]
        layout = go.Layout(
            title=title,
            xaxis=dict(title=x_label),
            yaxis=dict(title=y_label),
            bargap=0.2
        )
        fig = go.Figure(data=data, layout=layout)
        Display_Data.display_results(fig, 'histogram.html')
