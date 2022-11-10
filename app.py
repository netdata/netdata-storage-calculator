#%%

import streamlit as st

#%%

############################
# constants
############################

PER_METRIC_BYTES_64BIT = 165
PER_PAGE_BYTES_64BIT = 90
PER_EXTENT_BYTES_64BIT = 32
PER_FILE_BYTES_64BIT = 88
CACHE_OVERHEAD_PER_PAGE_BYTES_64BIT = 144
DISK_OVERHEAD_PERCENTAGE_64BIT = 0.11
TIER_EVERY_ITERATIONS = 60
COMPRESSION_DECREASE_PER_TIER = 0.1
EPHEMERAL_METRICS_PER_DAY = 0.05
BYTES_PER_METRIC_TIER_0 = 4
BYTES_PER_METRIC_TIER_1 = 16
BYTES_PER_METRIC_TIER_2 = 16
PAGE_SIZE_TIER_0 = 16384
PAGE_SIZE_TIER_1 = 8192
PAGE_SIZE_TIER_2 = 4096
PAGES_PER_EXTENT_TIER_0 = 4
PAGES_PER_EXTENT_TIER_1 = 8
PAGES_PER_EXTENT_TIER_2 = 16
COMPRESSION_SAVINGS_TIER_0 = 0.7
COMPRESSION_SAVINGS_TIER_1 = 0.7
COMPRESSION_SAVINGS_TIER_2 = 0.7

#%%

# title & logo
st.image('static/logo.png', width=400)
st.header('Netdata Storage Calculator')

# description
description = """
Experiment with the inputs below to come up with the best settings for your use case. 

Be sure to [read the docs](https://learn.netdata.cloud/docs/store/change-metrics-storage) first.
"""
st.markdown(description)

############################
# inputs
############################

st.subheader('Inputs')

# average_concurrent_metrics
average_concurrent_metrics = st.number_input('average concurrent metrics', value=2500, help='todo')

# maximum_disk_size_mb
c1r1, c2r1, c3r1 = st.columns(3)
maximum_disk_size_mb_tier_0 = c1r1.number_input('maximum disk size (MB) - Tier 0', value=1024, help='todo')
maximum_disk_size_mb_tier_1 = c2r1.number_input('maximum disk size (MB) - Tier 1', value=384, help='todo')
maximum_disk_size_mb_tier_2 = c3r1.number_input('maximum disk size (MB) - Tier 2', value=192, help='todo')

# update_every_sec
c1r2, c2r2, c3r2 = st.columns(3)
update_every_sec_tier_0 = c1r2.number_input('update every (sec) - Tier 0', value=1, help='todo')
update_every_sec_tier_1 = c2r2.number_input('update every (sec) - Tier 1', value=60, help='todo')
update_every_sec_tier_2 = c3r2.number_input('update every (sec) - Tier 2', value=3600, help='todo')

# page_cache_size_mb
c1r3, c2r3, c3r3 = st.columns(3)
page_cache_size_mb_tier_0 = c1r3.number_input('page cache size (MB)  - Tier 0', value=64, help='todo')
page_cache_size_mb_tier_1 = c2r3.number_input('page cache size (MB)  - Tier 1', value=36, help='todo')
page_cache_size_mb_tier_2 = c3r3.number_input('page cache size (MB)  - Tier 2', value=36, help='todo')

#%%

############################
# calculations
############################

observed_average_granularity_secs_tier_0 = update_every_sec_tier_0 * 1.2
observed_average_granularity_secs_tier_1 = update_every_sec_tier_1 * 1.2
observed_average_granularity_secs_tier_2 = update_every_sec_tier_2 * 1.2

page_cache_size_in_bytes_tier_0 = page_cache_size_mb_tier_0 * 1024 * 1024
page_cache_size_in_bytes_tier_1 = page_cache_size_mb_tier_1 * 1024 * 1024
page_cache_size_in_bytes_tier_2 = page_cache_size_mb_tier_2 * 1024 * 1024

max_full_pages_in_cache_tier_0 = page_cache_size_in_bytes_tier_0 / PAGE_SIZE_TIER_0
max_full_pages_in_cache_tier_1 = page_cache_size_in_bytes_tier_1 / PAGE_SIZE_TIER_1
max_full_pages_in_cache_tier_2 = page_cache_size_in_bytes_tier_2 / PAGE_SIZE_TIER_2

cache_overhead_in_bytes_tier_0 = max_full_pages_in_cache_tier_0 * CACHE_OVERHEAD_PER_PAGE_BYTES_64BIT
cache_overhead_in_bytes_tier_1 = max_full_pages_in_cache_tier_1 * CACHE_OVERHEAD_PER_PAGE_BYTES_64BIT
cache_overhead_in_bytes_tier_2 = max_full_pages_in_cache_tier_2 * CACHE_OVERHEAD_PER_PAGE_BYTES_64BIT

total_page_cache_bytes_tier_0 = page_cache_size_in_bytes_tier_0 + cache_overhead_in_bytes_tier_0
total_page_cache_bytes_tier_1 = page_cache_size_in_bytes_tier_1 + cache_overhead_in_bytes_tier_1
total_page_cache_bytes_tier_2 = page_cache_size_in_bytes_tier_2 + cache_overhead_in_bytes_tier_2

uncompressed_disk_size_tier_0 = (maximum_disk_size_mb_tier_0 * (1 - DISK_OVERHEAD_PERCENTAGE_64BIT) * 1024 * 1024) / (1 - COMPRESSION_SAVINGS_TIER_0)
uncompressed_disk_size_tier_1 = (maximum_disk_size_mb_tier_1 * (1 - DISK_OVERHEAD_PERCENTAGE_64BIT) * 1024 * 1024) / (1 - COMPRESSION_SAVINGS_TIER_1)
uncompressed_disk_size_tier_2 = (maximum_disk_size_mb_tier_2 * (1 - DISK_OVERHEAD_PERCENTAGE_64BIT) * 1024 * 1024) / (1 - COMPRESSION_SAVINGS_TIER_2)

pages_tier_0 = uncompressed_disk_size_tier_0 / PAGE_SIZE_TIER_0
pages_tier_1 = uncompressed_disk_size_tier_1 / PAGE_SIZE_TIER_1
pages_tier_2 = uncompressed_disk_size_tier_2 / PAGE_SIZE_TIER_2

extents_tier_0 = pages_tier_0 / PAGES_PER_EXTENT_TIER_0
extents_tier_1 = pages_tier_1 / PAGES_PER_EXTENT_TIER_1
extents_tier_2 = pages_tier_2 / PAGES_PER_EXTENT_TIER_2

total_points_in_the_database_tier_0 = uncompressed_disk_size_tier_0 / BYTES_PER_METRIC_TIER_0
total_points_in_the_database_tier_1 = uncompressed_disk_size_tier_1 / BYTES_PER_METRIC_TIER_1
total_points_in_the_database_tier_2 = uncompressed_disk_size_tier_2 / BYTES_PER_METRIC_TIER_2

points_for_a_full_retention_metric_tier_0 = total_points_in_the_database_tier_0 / average_concurrent_metrics
points_for_a_full_retention_metric_tier_1 = total_points_in_the_database_tier_1 / average_concurrent_metrics
points_for_a_full_retention_metric_tier_2 = total_points_in_the_database_tier_2 / average_concurrent_metrics

metric_retention_secs_tier_0 = points_for_a_full_retention_metric_tier_0 * observed_average_granularity_secs_tier_0
metric_retention_secs_tier_1 = points_for_a_full_retention_metric_tier_1 * observed_average_granularity_secs_tier_1
metric_retention_secs_tier_2 = points_for_a_full_retention_metric_tier_2 * observed_average_granularity_secs_tier_2

metric_retention_hours_tier_0 = metric_retention_secs_tier_0 / 60 / 60
metric_retention_hours_tier_1 = metric_retention_secs_tier_1 / 60 / 60
metric_retention_hours_tier_2 = metric_retention_secs_tier_2 / 60 / 60

metric_retention_days_tier_0 = metric_retention_hours_tier_0 / 24
metric_retention_days_tier_1 = metric_retention_hours_tier_1 / 24
metric_retention_days_tier_2 = metric_retention_hours_tier_2 / 24

maximum_number_of_unique_metrics_tier_0 = average_concurrent_metrics + (average_concurrent_metrics * EPHEMERAL_METRICS_PER_DAY * metric_retention_days_tier_0)
maximum_number_of_unique_metrics_tier_1 = average_concurrent_metrics + (average_concurrent_metrics * EPHEMERAL_METRICS_PER_DAY * metric_retention_days_tier_1)
maximum_number_of_unique_metrics_tier_2 = average_concurrent_metrics + (average_concurrent_metrics * EPHEMERAL_METRICS_PER_DAY * metric_retention_days_tier_2)

metrics_structures_bytes_tier_0 = (maximum_number_of_unique_metrics_tier_0 * PER_METRIC_BYTES_64BIT) if maximum_disk_size_mb_tier_0 > 0 else 0
metrics_structures_bytes_tier_1 = (maximum_number_of_unique_metrics_tier_1 * PER_METRIC_BYTES_64BIT) if maximum_disk_size_mb_tier_1 > 0 else 0
metrics_structures_bytes_tier_2 = (maximum_number_of_unique_metrics_tier_2 * PER_METRIC_BYTES_64BIT) if maximum_disk_size_mb_tier_2 > 0 else 0

pages_structures_bytes_tier_0 = pages_tier_0 * PER_PAGE_BYTES_64BIT
pages_structures_bytes_tier_1 = pages_tier_1 * PER_PAGE_BYTES_64BIT
pages_structures_bytes_tier_2 = pages_tier_2 * PER_PAGE_BYTES_64BIT

extents_structures_bytes_tier_0 = extents_tier_0 * PER_EXTENT_BYTES_64BIT
extents_structures_bytes_tier_1 = extents_tier_1 * PER_EXTENT_BYTES_64BIT
extents_structures_bytes_tier_2 = extents_tier_2 * PER_EXTENT_BYTES_64BIT

dbengine_index_memory_mb_tier_0 = (metrics_structures_bytes_tier_0 + pages_structures_bytes_tier_0 + extents_structures_bytes_tier_0) / 1024 / 1024
dbengine_index_memory_mb_tier_1 = (metrics_structures_bytes_tier_1 + pages_structures_bytes_tier_1 + extents_structures_bytes_tier_1) / 1024 / 1024
dbengine_index_memory_mb_tier_2 = (metrics_structures_bytes_tier_2 + pages_structures_bytes_tier_2 + extents_structures_bytes_tier_2) / 1024 / 1024

collectors_memory_mb_tier_0 = (PAGE_SIZE_TIER_0 * average_concurrent_metrics) / 1024 / 1024
collectors_memory_mb_tier_1 = (PAGE_SIZE_TIER_1 * average_concurrent_metrics) / 1024 / 1024
collectors_memory_mb_tier_2 = (PAGE_SIZE_TIER_2 * average_concurrent_metrics) / 1024 / 1024

final_page_cache_size_in_mb_tier_0 = total_page_cache_bytes_tier_0 / 1024 / 1024
final_page_cache_size_in_mb_tier_1 = total_page_cache_bytes_tier_1 / 1024 / 1024
final_page_cache_size_in_mb_tier_2 = total_page_cache_bytes_tier_2 / 1024 / 1024

total_ram_memory_mb_tier_0 = dbengine_index_memory_mb_tier_0 + collectors_memory_mb_tier_0 + final_page_cache_size_in_mb_tier_0
total_ram_memory_mb_tier_1 = dbengine_index_memory_mb_tier_1 + collectors_memory_mb_tier_1 + final_page_cache_size_in_mb_tier_1
total_ram_memory_mb_tier_2 = dbengine_index_memory_mb_tier_2 + collectors_memory_mb_tier_2 + final_page_cache_size_in_mb_tier_2

############################
# estimated outputs
############################

estimated_data_points_stored = total_points_in_the_database_tier_0 + total_points_in_the_database_tier_1 + total_points_in_the_database_tier_2
estimated_points_per_metric = points_for_a_full_retention_metric_tier_0 + points_for_a_full_retention_metric_tier_1 + points_for_a_full_retention_metric_tier_2
estimated_maximum_days = metric_retention_days_tier_2
estimated_disk_storage_gb = (maximum_disk_size_mb_tier_0 + maximum_disk_size_mb_tier_1 + maximum_disk_size_mb_tier_2) / 1024
estimated_ram_mb = total_ram_memory_mb_tier_0 + total_ram_memory_mb_tier_1 + total_ram_memory_mb_tier_2
estimated_dbengine_tier_1_update_every_iterations = update_every_sec_tier_1 / update_every_sec_tier_0
estimated_dbengine_tier_2_update_every_iterations = update_every_sec_tier_2 / update_every_sec_tier_1

#%% 

############################
# outputs
############################

st.subheader('Outputs')

output_message = f'Netdata will store an estimated **{round(estimated_data_points_stored):000,}** data points (**{round(estimated_points_per_metric):000,} points/metric**) '
output_message += f'for a maximum of **{round(estimated_maximum_days):000,} days**, utilizing **{round(estimated_disk_storage_gb,2):000,} GB** of disk storage '
output_message += f'and **{round(estimated_ram_mb):000,} MB** of RAM.'

output_netdata_conf = f"""
# Enter the following in your agent's netdata.conf
[db]
  mode = dbengine
  storage tiers = 3
  update every = {update_every_sec_tier_0}
  dbengine multihost disk space MB = {maximum_disk_size_mb_tier_0}
  dbengine page cache size MB = {page_cache_size_mb_tier_0}
  dbengine tier 1 update every iterations = {round(estimated_dbengine_tier_1_update_every_iterations)}
  dbengine tier 1 multihost disk space MB = {maximum_disk_size_mb_tier_1}
  dbengine tier 1 page cache size MB = {page_cache_size_mb_tier_1}
  dbengine tier 2 update every iterations = {round(estimated_dbengine_tier_2_update_every_iterations)}
  dbengine tier 2 multihost disk space MB = {maximum_disk_size_mb_tier_2}
  dbengine tier 2 page cache size MB = {page_cache_size_mb_tier_2}
"""

# message
st.write(output_message)

# conf
st.code(output_netdata_conf, language='ini')

#%%
