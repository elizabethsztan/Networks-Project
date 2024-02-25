#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 13:14:23 2023

@author: liz
"""

"""
TASK 3.3: degree distribution
"""

#load in all of the data
k_array3_file = np.load('backup_data/task_3_3_new/degree_distribution_m3_I5.npz')
k_array3 = unpack_npz(k_array3_file, integer = True)
k_array9_file = np.load('backup_data/task_3_3_new/degree_distribution_m9_I5.npz')
k_array9 = unpack_npz(k_array9_file, integer = True)
k_array27_file = np.load('backup_data/task_3_3_new/degree_distribution_m27_I5.npz')
k_array27 = unpack_npz(k_array27_file, integer = True)

#%% smooth/find average of the data by combining all runs and logbinning

cc = 0 #for the colors

for array in (k_array3, k_array9, k_array27):
    m = min(array[0])
    m = m*(3)
    flat_array = np.array(array).flatten().astype(int)
    x, y = logbin(flat_array, 1.07) #gives the degree and probability of degree 
    plt.plot(x, y, 'o', color = 'black', markerfacecolor = color_cycler[cc], label = r'$m = %d$' %(m), markeredgewidth = 0.5, ms=4)
    #plot theoretical distribution
    x1,y1 = theoretical_k_dist_EV(m, flat_array)
    plt.plot(x1, y1, color = color_cycler[cc], linestyle = '--')
    cc+=1

#plt.title('Existing Vertices: Degree Distribution')

plt.plot([],[], color = 'black', ls = '--', label = r'$p_\infty(k)$')

plt.legend()
plt.xlabel(r'$k$')
plt.ylabel(r'$p(k)$')
plt.yscale('log')
plt.xscale('log')

plt.savefig('images/EV degree dist', dpi = 500)

#%% KS test on the data

cc = 0 #for the colors

for array in (k_array3, k_array9, k_array27):
    m = min(array[0])
    m = m*(3)
    flat_array = np.array(array).flatten()
    x, y = logbin(flat_array) #gives the degree and probability of degree 
    y=np.cumsum(np.array(y))
    plt.plot(np.log(x), y, 'o',color = color_cycler[cc], label = r'$m = %d$' %(m), markeredgewidth = 0.1, ms = 3)
    #plot theoretical distribution
    x1,y1 = theoretical_k_dist_EV(m, flat_array, cum = True)
    plt.plot(np.log(x1), y1, color = color_cycler[cc], linestyle = '--')
    #ks test on the data 
    ks_stat = max(abs(y1-y))
    p_value = stats.kstwo.sf(ks_stat, len(flat_array))
    print('m: '+ str(m))
    print('k_stat: ' + str(ks_stat))
    print('p_value: '+ str(p_value))
    cc+=1

plt.plot([],[], color = 'black', ls = '--', label = r'$p_\infty(k)$')

#plt.title('Random Attachment: Degree Distribution CDF')
plt.legend()
plt.xlabel(r'$k_0$')
plt.ylabel(r'$p(k>k_0)$')

plt.savefig('images/EV degree dist CDF', dpi = 500)

#%%

"""
TASK 2.4: Finite-size effect
"""
k_array_file = np.load('backup_data/task_3_4/degree_distribution_m3_I10.npz')
k_array = unpack_npz(k_array_file, integer = True)
N_array = [100,1000,10000,100000]

k_array_divided = []
for i in range(len(k_array)):
    temp = []
    divider = int(len(k_array[i])/10)
    for X in range (1,11):
        temp.append(k_array[i][int((X-1)*divider):int((X*divider))])
    k_array_divided.append(temp)
#k_array_divided is split up into k_array_divided[N from N array][iteration out of 10]

#to improve statistics, average all 10 runs 
k_array_av = []
for N in k_array_divided:
    temp = []
    for run in N:
        temp.append (run)
    temp = np.array(temp).flatten()
    k_array_av.append(temp)



#%% plot different N
cc = 0

for array in k_array_av:
    x, y = logbin (array, 1.06)
    plt.plot(x, y, 'o',color = 'black', markerfacecolor = color_cycler[cc], label = r'$N = %d$' %(N_array[cc]), markeredgewidth = 0.5, ms = 4)
    cc += 1
    
#fit the theoretical dist onto the data 
x1, y1 = theoretical_k_dist_EV(3, k_array_av[-1], cum = False)
plt.plot(x1,y1, '--', color = 'black', label = r'$p_\infty(k)$')

#plt.title('Random Attachment: Degree Distribution m = 128')
plt.legend()
plt.xlabel(r'$k$')
plt.ylabel(r'$p(k)$')
plt.yscale('log')
plt.xscale('log')

plt.savefig('images/EV finite size effect', dpi = 500)

#%%

k1_array_calc = [] #an array of k1 for each iteration


for N in k_array_divided:
    temp = []
    for run in N:
        temp.append(np.max(np.array(run)))
    temp=np.array(temp).flatten()
    k1_array_calc.append(temp)


#find the mean and std for each N value
k1_mean = []
k1_std = []
# k1_max = []
# k1_min = []
# k1_upper = []
# k1_lower = []




for array in k1_array_calc:
    k1_mean.append(np.mean(array))
    k1_std.append(np.std(array))
    
    k1_max.append (np.max(array))
    k1_min.append (np.min(array))



#find theoretical k1 
theor_k1_array = []


for n in N_array:
    theor_k1_array.append(find_theoretical_k1_EV(n,3))

    
#fit a linear line to the data
#for RA, a plot of k1 by log(N) gives a straight line

k1_mean_fit, k1_mean_cov = np.polyfit(np.log(N_array), np.log(k1_mean), 1, cov = True)
pfit1=np.poly1d(k1_mean_fit)

theor_k1_fit, theor_k1_cov = np.polyfit(np.log(N_array), np.log(theor_k1_array), 1, cov = True)
pfit2=np.poly1d(theor_k1_fit)


plt.plot(N_array, np.exp(pfit1(np.log(N_array))), ls = '-', color = color_cycler[0], label = 'm=3') #m=3
plt.plot(N_array, np.exp(pfit2(np.log(N_array))), ls = ':', color = color_cycler[0], label = r'$k_1^\star$') #theor


k1_mean_uncer = get_uncertainties(k1_mean_cov)
theor_k1_uncer = get_uncertainties(theor_k1_cov)

plt.errorbar(N_array, k1_mean,yerr = k1_std, ls = '', color = color_cycler[0])
#plt.plot(N_array, theor_k1_array, color = color_cycler[0], ls = '-', label = 'Theoretical', ms = 3)



plt.xlabel(r'$N$')
plt.ylabel(r'$k_1(N,m)$')
plt.legend()
#plt.title('Random Attachment: '+r'$k_1$')

plt.xscale('log')
plt.yscale('log')
print('Calculated')
print('y = ( %f +/- %f ) x+ ( %f +/- %f )' %(k1_mean_fit[0], k1_mean_uncer[0], k1_mean_fit[1], k1_mean_uncer[1]))
print('Theoretical')
print('y = ( %f +/- %f ) x + ( %f +/- %f )' %(theor_k1_fit[0], theor_k1_uncer[0], theor_k1_fit[1], theor_k1_uncer[0]))

plt.savefig('images/EV k1 plots', dpi = 500)


#%% Data collapse

cc = 0

for array in k_array_av:
    x, y = logbin (array, 1.06)
    y1 = find_theoretical_pk_EV(x, 3)
    y=np.divide(y, y1)
    #x=np.divide(x, k1_mean[cc]) 
    x=np.divide(x, theor_k1_array[cc])
    plt.plot(x, y, 'o',color = 'black', markerfacecolor = color_cycler[cc], label = r'$N = %d$' %(N_array[cc]), markeredgewidth = 0.5, ms = 4)
    cc += 1
    

#plt.title('Random Attachment: Data Collapse')
plt.legend()
plt.xlabel(r'$k/k_1$')
plt.ylabel(r'$p(k)/p_\infty (k)$')
plt.yscale('log')
plt.xscale('log')
#plt.xlim(0,0.8)
#plt.xscale('log')

#plt.savefig('images/EV data collapse sim', dpi = 500)
plt.savefig('images/EV data collapse theor mod', dpi = 500)
