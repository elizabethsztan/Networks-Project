#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 10:04:16 2023

@author: liz
"""
params = {
    'axes.labelsize': 25,
    'font.size': 25,
    'legend.fontsize': 15,
    'figure.figsize': [10,8],
    'xtick.labelsize': 25,
    'ytick.labelsize': 25
    }
plt.rcParams.update(params)


#%%

"""
TASK 1.3: degree distribution
"""

#load in all of the data
k_array4_file = np.load('backup_data/task_1_3/degree_distribution_m4_I10.npz')
k_array4 = unpack_npz(k_array4_file, integer = True)
k_array8_file = np.load('backup_data/task_1_3/degree_distribution_m8_I10.npz')
k_array8 = unpack_npz(k_array8_file, integer = True)
k_array16_file = np.load('backup_data/task_1_3/degree_distribution_m16_I10.npz')
k_array16 = unpack_npz(k_array16_file, integer = True)
k_array32_file = np.load('backup_data/task_1_3/degree_distribution_m32_I10.npz')
k_array32 = unpack_npz(k_array32_file, integer = True)
k_array64_file = np.load('backup_data/task_1_3/degree_distribution_m64_I10.npz')
k_array64 = unpack_npz(k_array64_file, integer = True)
k_array128_file = np.load('backup_data/task_1_3/degree_distribution_m128_I10.npz')
k_array128 = unpack_npz(k_array128_file, integer = True)
k_array256_file = np.load('backup_data/task_1_3/degree_distribution_m256_I10.npz')
k_array256 = unpack_npz(k_array256_file, integer = True)
#%%

"""
degree distribution: superhub
"""

#load in all of the data
k_array4_file = np.load('backup_data/task_1_3/superhub/degree_distribution_m4_I3.npz')
k_array4 = unpack_npz(k_array4_file, integer = True)
k_array8_file = np.load('backup_data/task_1_3/superhub/degree_distribution_m8_I3.npz')
k_array8 = unpack_npz(k_array8_file, integer = True)
k_array16_file = np.load('backup_data/task_1_3/superhub/degree_distribution_m16_I3.npz')
k_array16 = unpack_npz(k_array16_file, integer = True)
k_array32_file = np.load('backup_data/task_1_3/superhub/degree_distribution_m32_I3.npz')
k_array32 = unpack_npz(k_array32_file, integer = True)
k_array64_file = np.load('backup_data/task_1_3/superhub/degree_distribution_m64_I3.npz')
k_array64 = unpack_npz(k_array32_file, integer = True)
k_array128_file = np.load('backup_data/task_1_3/superhub/degree_distribution_m128_I3.npz')
k_array128 = unpack_npz(k_array128_file, integer = True)
k_array256_file = np.load('backup_data/task_1_3/superhub/degree_distribution_m256_I3.npz')
k_array256 = unpack_npz(k_array256_file, integer = True)
#%%

"""
degree distribution: sparse
"""

#load in all of the data
k_array4_file = np.load('backup_data/task_1_3/sparse/degree_distribution_m4_I3.npz')
k_array4 = unpack_npz(k_array4_file, integer = True)
k_array8_file = np.load('backup_data/task_1_3/sparse/degree_distribution_m8_I3.npz')
k_array8 = unpack_npz(k_array8_file, integer = True)
k_array16_file = np.load('backup_data/task_1_3/sparse/degree_distribution_m16_I3.npz')
k_array16 = unpack_npz(k_array16_file, integer = True)
k_array32_file = np.load('backup_data/task_1_3/sparse/degree_distribution_m32_I3.npz')
k_array32 = unpack_npz(k_array32_file, integer = True)
k_array64_file = np.load('backup_data/task_1_3/sparse/degree_distribution_m64_I3.npz')
k_array64 = unpack_npz(k_array32_file, integer = True)
k_array128_file = np.load('backup_data/task_1_3/sparse/degree_distribution_m128_I3.npz')
k_array128 = unpack_npz(k_array128_file, integer = True)
k_array256_file = np.load('backup_data/task_1_3/sparse/degree_distribution_m256_I3.npz')
k_array256 = unpack_npz(k_array256_file, integer = True)

#%% smooth/find average of the data by combining all runs and logbinning

cc = 0 #for the colors

for array in (k_array4, k_array8, k_array16, k_array32, k_array64, k_array128, k_array256):
#for array in (k_array4, k_array8, k_array16, k_array32):
    m = min(array[0])
    flat_array = np.array(array).flatten()
    x, y = logbin(flat_array, 1.1) #gives the degree and probability of degree 
    plt.loglog(x, y, 'o', color = 'black', markerfacecolor = color_cycler[cc], label = r'$m = %d$' %(m), markeredgewidth = 0.5, ms = 4)
    #plot theoretical distribution
    x1,y1 = theoretical_k_dist_PA(m, flat_array)
    plt.loglog(x1, y1, color = color_cycler[cc], linestyle = '--')
    
    cc+=1
plt.plot([],[], color = 'black', ls = '--', label = r'$p_\infty(k)$')
#plt.title('Preferential Attachment: Degree Distribution')
plt.legend()
plt.xlabel(r'$k$')
plt.ylabel(r'$p(k)$')

# plt.savefig('images/PA degree dist sparse', dpi = 500)
# plt.savefig('images/PA degree dist superhub', dpi = 500)
# plt.savefig('images/PA degree dist', dpi = 500)

#%% KS test on the data

cc = 0 #for the colors

for array in (k_array4, k_array8, k_array16, k_array32, k_array64, k_array128, k_array256):
    m = min(array[0])
    flat_array = np.array(array).flatten()
    x, y = logbin(flat_array) #gives the degree and probability of degree 
    y=np.cumsum(np.array(y))
    plt.plot(np.log(x), y, 'o', markerfacecolor = color_cycler[cc], label = r'$m = %d$' %(m), markeredgewidth = 0.08, ms = 3)
    #plot theoretical distribution
    x1,y1 = theoretical_k_dist_PA(m, flat_array, cum = True)
    plt.plot(np.log(x1), y1, color = color_cycler[cc], linestyle = '--')
    #ks test on the data 
    ks_stat = max(abs(y1-y))
    p_value = stats.kstwo.sf(ks_stat, len(flat_array))
    print('m: '+ str(m))
    print('k_stat: ' + str(ks_stat))
    print('p_value: '+ str(p_value))
    print('len vals: '+ str(len(flat_array)))
    cc+=1
plt.plot([],[], color = 'black', ls = '--', label = r'$p_\infty(k)$')
#plt.title('Preferential Attachment: Degree Distribution CDF')
plt.legend()
plt.xlabel(r'$k_0$')
plt.ylabel(r'$p(k>k_0)$')

plt.savefig('images/PA degree dist CDF', dpi = 500)

#%%

"""
TASK 1.4: Finite-size effect
"""
k_array_file = np.load('backup_data/task_1_4/degree_distribution_m128_I10.npz')
k_array = unpack_npz(k_array_file, integer = True)

k_array_file64 = np.load('backup_data/task_1_4/degree_distribution_m64_I10.npz')
k_array64 = unpack_npz(k_array_file64, integer = True)

k_array_file4 = np.load('backup_data/task_1_4/degree_distribution_m4_I10.npz')
k_array4 = unpack_npz(k_array_file4, integer = True)

N_array = [100,1000,10000,100000,1000000]

k_array_divided = []
k_array_divided64 = []
k_array_divided4 = []

for i in range(len(k_array)):
    temp = []
    divider = int(len(k_array[i])/10)
    for X in range (1,11):
        temp.append(k_array[i][int((X-1)*divider):int((X*divider))])
    k_array_divided.append(temp)
   
for i in range(len(k_array64)):
    temp = []
    divider = int(len(k_array64[i])/10)
    for X in range (1,11):
        temp.append(k_array64[i][int((X-1)*divider):int((X*divider))])
    k_array_divided64.append(temp)
    
for i in range(len(k_array4)):
    temp = []
    divider = int(len(k_array4[i])/10)
    for X in range (1,11):
        temp.append(k_array4[i][int((X-1)*divider):int((X*divider))])
    k_array_divided4.append(temp)
    
#k_array_divided is split up into k_array_divided[N from N array][iteration out of 10]

#to improve statistics, average all 10 runs 
k_array_av = []
k_array_av64 = []
k_array_av4 = []

for N in k_array_divided:
    temp = []
    for run in N:
        temp.append (run)
    temp = np.array(temp).flatten()
    k_array_av.append(temp)
    
for N in k_array_divided4:
    temp = []
    for run in N:
        temp.append (run)
    temp = np.array(temp).flatten()
    k_array_av4.append(temp)

for N in k_array_divided64:
    temp = []
    for run in N:
        temp.append (run)
    temp = np.array(temp).flatten()
    k_array_av64.append(temp)



#%% plot different N
cc = 0

for array in k_array_av:
    x, y = logbin (array, 1.03)
    plt.plot(x, y, 'o',color = 'black', markerfacecolor = color_cycler[cc], label = r'$N = %d$' %(N_array[cc]), markeredgewidth = 0.5, ms = 4)
    cc += 1
    
#fit the theoretical dist onto the data 
x1, y1 = theoretical_k_dist_PA(128, k_array_av[-1])
plt.loglog(x1,y1, '--', color = 'black', label = r'$p_\infty(k)$')

#plt.title('Preferential Attachment: Degree Distribution m = 128')
plt.legend()
plt.xlabel(r'$k$')
plt.ylabel(r'$p(k)$')
#plt.savefig('images/PA finite size effect', dpi = 500)

#%% find the theoretical and calculated k1

k1_array_calc = [] #an array of k1 for each iteration
k1_array_calc4 = []
k1_array_calc64 = []

for N in k_array_divided:
    temp = []
    for run in N:
        temp.append(np.max(np.array(run)))
    temp=np.array(temp).flatten()
    k1_array_calc.append(temp)

for N in k_array_divided4:
    temp = []
    for run in N:
        temp.append(np.max(np.array(run)))
    temp=np.array(temp).flatten()
    k1_array_calc4.append(temp)

for N in k_array_divided64:
    temp = []
    for run in N:
        temp.append(np.max(np.array(run)))
    temp=np.array(temp).flatten()
    k1_array_calc64.append(temp)

#find the mean and std for each N value
k1_mean = []
k1_std = []
#k1_max = []
#k1_min = []
#k1_upper = []
#k1_lower = []

k1_mean4 = []
k1_std4 = []

k1_mean64 = []
k1_std64 = []

for array in k1_array_calc:
    k1_mean.append(np.mean(array))
    k1_std.append(np.std(array))

for array in k1_array_calc4:
    k1_mean4.append(np.mean(array))
    k1_std4.append(np.std(array))

for array in k1_array_calc64:
    k1_mean64.append(np.mean(array))
    k1_std64.append(np.std(array))
    
    #k1_max.append (np.max(array))
    #k1_min.append (np.min(array))

#k1_upper = np.subtract(k1_max, k1_mean)
#k1_lower = np.subtract(k1_mean, k1_min)

#find theoretical k1 
theor_k1_array = []
theor_k1_array4 = []
theor_k1_array64 = []

theor_k1_array_mod = []
theor_k1_array4_mod = []
theor_k1_array64_mod = []

for n in N_array:
    theor_k1_array.append(find_theoretical_k1_PA(n, 128))
    theor_k1_array4.append(find_theoretical_k1_PA(n, 4))
    theor_k1_array64.append(find_theoretical_k1_PA(n, 64))
    
    theor_k1_array_mod.append(find_theoretical_k1_PA(n, 128, mod = True))
    theor_k1_array4_mod.append(find_theoretical_k1_PA(n, 4, mod = True))
    theor_k1_array64_mod.append(find_theoretical_k1_PA(n, 64, mod = True))
    

    
#fit a linear line to the data

#m = 4

k1_mean_fit4, k1_mean_cov4 = np.polyfit(np.log(N_array), np.log(k1_mean4), 1, cov = True)
pfit1_4=np.poly1d(k1_mean_fit4)

theor_k1_fit4, theor_k1_cov4 = np.polyfit(np.log(N_array), np.log(theor_k1_array4), 1, cov = True)
pfit2_4=np.poly1d(theor_k1_fit4)

theor_k1_fit4_mod, theor_k1_cov4_mod = np.polyfit(np.log(N_array), np.log(theor_k1_array4_mod), 1, cov = True)
pfit2_4_mod=np.poly1d(theor_k1_fit4_mod)

plt.plot(N_array, np.exp(pfit1_4(np.log(N_array))), ls = '-', color = color_cycler[1],label = r'$m=4$')
plt.plot(N_array, np.exp(pfit2_4(np.log(N_array))), ls = '--', color = color_cycler[1])
plt.plot(N_array, np.exp(pfit2_4_mod(np.log(N_array))), ls = ':', color = color_cycler[1])

k1_mean_uncer4 = get_uncertainties(k1_mean_cov4)
theor_k1_uncer4 = get_uncertainties(theor_k1_cov4)
theor_k1_uncer4_mod = get_uncertainties(theor_k1_cov4_mod)

#m=64

k1_mean_fit64, k1_mean_cov64 = np.polyfit(np.log(N_array), np.log(k1_mean64), 1, cov = True)
pfit1_64=np.poly1d(k1_mean_fit64)

theor_k1_fit64, theor_k1_cov64 = np.polyfit(np.log(N_array), np.log(theor_k1_array64), 1, cov = True)
pfit2_64=np.poly1d(theor_k1_fit64)

theor_k1_fit64_mod, theor_k1_cov64_mod = np.polyfit(np.log(N_array), np.log(theor_k1_array64_mod), 1, cov = True)
pfit2_64_mod=np.poly1d(theor_k1_fit64_mod)

plt.plot(N_array, np.exp(pfit1_64(np.log(N_array))), ls = '-', color = color_cycler[2],label = r'$m=64$')
plt.plot(N_array, np.exp(pfit2_64(np.log(N_array))), ls = '--', color = color_cycler[2])
plt.plot(N_array, np.exp(pfit2_64_mod(np.log(N_array))), ls = ':', color = color_cycler[2])

k1_mean_uncer64 = get_uncertainties(k1_mean_cov64)
theor_k1_uncer64 = get_uncertainties(theor_k1_cov64)
theor_k1_uncer64_mod = get_uncertainties(theor_k1_cov64_mod)

#m=128

k1_mean_fit, k1_mean_cov = np.polyfit(np.log(N_array), np.log(k1_mean), 1, cov = True)
pfit1=np.poly1d(k1_mean_fit)

theor_k1_fit, theor_k1_cov = np.polyfit(np.log(N_array), np.log(theor_k1_array), 1, cov = True)
pfit2=np.poly1d(theor_k1_fit)

theor_k1_fit_mod, theor_k1_cov_mod = np.polyfit(np.log(N_array), np.log(theor_k1_array_mod), 1, cov = True)
pfit2_mod=np.poly1d(theor_k1_fit_mod)

plt.plot(N_array, np.exp(pfit1(np.log(N_array))), ls = '-', color = color_cycler[0],label = r'$m=128$')
plt.plot(N_array, np.exp(pfit2(np.log(N_array))), ls = '--', color = color_cycler[0])
plt.plot(N_array, np.exp(pfit2_mod(np.log(N_array))), ls = ':', color = color_cycler[0])

k1_mean_uncer = get_uncertainties(k1_mean_cov)
theor_k1_uncer = get_uncertainties(theor_k1_cov)
theor_k1_uncer_mod = get_uncertainties(theor_k1_cov_mod)

#plot rest of data

# plt.errorbar(np.log(N_array), np.log(k1_mean), ls = '', marker = 'o', label = 'Calculated')
# plt.plot(np.log(N_array), np.log(theor_k1_array), color = 'black', ls = '', marker='o', label = 'Theoretical')

plt.errorbar(N_array, k1_mean4, yerr = k1_std4, color = color_cycler[1], ls = '')

plt.errorbar(N_array, k1_mean64, yerr = k1_std64, color = color_cycler[2], ls = '')

plt.errorbar(N_array, k1_mean, yerr = k1_std, ls = '', color = color_cycler[0])
#plt.plot(N_array, theor_k1_array, ls = '',color = color_cycler[0])

plt.plot([],[], color = 'black', ls = '--', label = r'$k_1(N,m)$')
plt.plot([],[], color = 'black', ls = ':', label = r'$k_1^\star(N,m)$')

plt.xlabel(r'$N$')
plt.ylabel(r'$k_1(N,m)$')
plt.legend()
#plt.title('Preferential Attachment: '+r'$k_1$')

plt.xscale('log')
plt.yscale('log')

print('Simulated m = 128')
print('y = ( %f +/- %f ) x+ ( %f +/- %f )' %(k1_mean_fit[0], k1_mean_uncer[0], k1_mean_fit[1], k1_mean_uncer[1]))
print('Theoretical m = 128')
print('y = ( %f +/- %f ) x + ( %f +/- %f )' %(theor_k1_fit[0], theor_k1_uncer[0], theor_k1_fit[1], theor_k1_uncer[0]))

print('Simulated m = 64')
print('y = ( %f +/- %f ) x+ ( %f +/- %f )' %(k1_mean_fit64[0], k1_mean_uncer64[0], k1_mean_fit64[1], k1_mean_uncer64[1]))
print('Theoretical m = 64')
print('y = ( %f +/- %f ) x + ( %f +/- %f )' %(theor_k1_fit64[0], theor_k1_uncer64[0], theor_k1_fit64[1], theor_k1_uncer64[0]))

print('Simulated m = 4')
print('y = ( %f +/- %f ) x+ ( %f +/- %f )' %(k1_mean_fit4[0], k1_mean_uncer4[0], k1_mean_fit4[1], k1_mean_uncer4[1]))
print('Theoretical m = 4')
print('y = ( %f +/- %f ) x + ( %f +/- %f )' %(theor_k1_fit4[0], theor_k1_uncer4[0], theor_k1_fit4[1], theor_k1_uncer4[0]))

plt.savefig('images/PA k1 plots', dpi = 500)

#%% Data collapse

cc = 0

for array in k_array_av:
    x, y = logbin (array, 1.03)
    y1 = find_theoretical_pk_PA(x, 128)
    y=np.divide(y, y1)
    x=np.divide(x, k1_mean[cc]) 
    #x=np.divide(x, theor_k1_array[cc])
    #x=np.divide(x, theor_k1_array_mod[cc])
    plt.loglog(x, y, 'o',color = 'black', markerfacecolor = color_cycler[cc], label = r'$N = %d$' %(N_array[cc]), markeredgewidth = 0.5, ms = 4)
    cc += 1
    
x1, y1 = theoretical_k_dist_PA(128, k_array_av[-1])
y1=np.divide(y1, find_theoretical_pk_PA(x1, 128))
#x1=np.divide(x1, k1_mean[-1])
x1=np.divide(x1, theor_k1_array[-1])
#plt.loglog(x1,y1, '--', color = 'black', label = r'$p_\infty(k)$')

#plt.title('Preferential Attachment: Data Collapse')
plt.legend()
plt.xlabel(r'$k/k_1$')
plt.ylabel(r'$p(k)/p_\infty (k)$')
plt.savefig('images/PA data collapse sim', dpi = 500)
#plt.savefig('images/PA data collapse theor', dpi = 500)
#plt.savefig('images/PA data collapse theor mod', dpi = 500)





