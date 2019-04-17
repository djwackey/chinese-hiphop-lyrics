# chinese-hiphop-lyrics

## 格式化JSON文件
cat air.json | python -m json.tool

### 修正包含中文的JSON文件的格式化显示问题
1.编辑/usr/lib/python2.7/json/tool.py文件
注释下面两行
s = json.dump(obj, outfile, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
outfile.write('\n')
替换为下面两行
s = json.dumps(obj, sort_keys=True, indent=4, ensure_ascii=False)
outfile.write(codecs.encode(s, 'utf-8'))
