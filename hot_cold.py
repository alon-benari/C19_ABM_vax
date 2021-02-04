
def hot_cold_spots(y,gdf):
    '''
    Identify hot cold spots
    '''
    wq =  lps.weights.Queen.from_dataframe(gdf)
    wq.transform = 'r'
    lag_value = lps.weights.lag_spatial(wq, y)
        #

    b, a = np.polyfit(y, lag_value, 1)
    f, ax = plt.subplots(1, figsize=(6, 6))

    plt.plot(y, lag_value, '.', color='firebrick')

    # dashed vert at mean of the price
    plt.vlines(y.mean(), lag_value.min(), lag_value.max(), linestyle='--')
    # dashed horizontal at mean of lagged price 
    plt.hlines(lag_value.mean(), y.min(),y.max(), linestyle='--')

    # red line of best fit using global I as slope
    plt.plot(y, a + b*y, 'r')
    plt.show()

    li = esda.moran.Moran_Local(y, wq)
    sig = 1 * (li.p_sim < 0.05)
    hotspot = 1 * (sig * li.q==1)
    coldspot = 3 * (sig * li.q==3)
    doughnut = 2 * (sig * li.q==2)
    diamond = 4 * (sig * li.q==4)
    spots = hotspot + coldspot + doughnut + diamond

    spot_labels = [ '0 ns', '1 hot spot', '2 doughnut', '3 cold spot', '4 diamond']
    labels = [spot_labels[i] for i in spots]
    from matplotlib import colors
    hmap = colors.ListedColormap([ 'lightgrey', 'red', 'lightblue', 'blue', 'pink'])
    f, ax = plt.subplots(1, figsize=(9, 9))
    gdf.assign(cl=labels).plot(column='cl', categorical=True, \
            k=2, cmap=hmap, linewidth=0.1, ax=ax, \
            edgecolor='white', legend=True)
    ax.set_axis_off()
    ax.set_title(y.name+"_HotColdSpots")
    plt.show()
