import pstats

# Load the profiling data from the generated file
p = pstats.Stats('profile_output.prof')

# Sort the statistics by cumulative time and print the top 10 results
p.sort_stats('cumulative').print_stats(10)