import platform
print(platform.python_implementation())


vs_M = ['saih', 'saicfh', 'saicfeh', 'saicfedgh', 'sajih', 'sajicfh', 'sajicfeh', 'sajicfedgh', 'saeh', 'saefh', 'saefcih', 'saedgh', 'sacih', 'sacfh', 'sacfeh', 'sacfedgh', 'sabdgh', 'sabdeh', 'sabdefh', 'sabdefcih']

vp_M = ['psaih', 'psaicfh', 'psaicfeh', 'psaicfedgh', 'psajih', 'psajicfh', 'psajicfeh', 'psajicfedgh', 'psaeh', 'psaefh', 'psaefcih', 'psaedgh', 'psacih', 'psacfh', 'psacfeh', 'psacfedgh', 'psabdgh', 'psabdeh', 'psabdefh', 'psabdefcih']

vp_S = ['psabdefcih', 'psabdefh', 'psabdeh', 'psabdgh', 'psacfedgh', 'psacfeh', 'psacfh', 'psacih', 'psaedgh', 'psaefcih', 'psaefh', 'psaeh', 'psaicfedgh', 'psaicfeh', 'psaicfh', 'psaih', 'psajicfedgh', 'psajicfeh', 'psajicfh', 'psajih']

ground_truth = True

print ('vp_M: {} solutions'.format(len(vp_M)))
print ('vp_S: {} solutions'.format(len(vp_S)))
print ('SHOULD BE {} SOLUTIONS'.format(ground_truth))


print('abc'.split(''))
