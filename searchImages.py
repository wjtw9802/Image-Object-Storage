import searchMinio
import searchSQL

print('You are about to search images')
results, decision = searchSQL.sqlConnect()
if len(results) == 0:
    exit()
searchMinio.getImages(results, decision)