from typing import List
from ruamel.yaml import YAML


class FileYaml:
	def __init__(self, flag: int, name: str, attr: list) -> None:
		self.file = {
			"path":f"./{name}.csv",
			"failDataPath":f"./err/{name}.csv",
			"batchSize":2,
			"inOrder":False,
			"type":"csv",
			"csv":{
				"withHeader":False,
				"withLabel":False
			},
			"schema": None
		}
		if flag == 0:		# vertex
			self.file["schema"] = {
				"type":"vertex",
				"vertex":{
					"vid":{
						"type":"string"
					},
					"tags":[
						{
							"name":name,
							"props":attr
						}
					]
				}
			}
		elif flag == 1:		# edge
			self.file["schema"] = {
				"type":"edge",
				"edge":{
					"name":name,
					"withRanking":False,
					"srcVID":{
						"type":"string"
					},
					"dstVID":{
						"type":"string"
					},
					"props":[]
				}
			}


class CreateYaml:
	def __init__(self, space: str, files: List[FileYaml], sql: list, concurrency=1, user="chengrong", password=780128, address="127.0.0.1:9669") -> None:
		commands = ["UPDATE CONFIGS storage:wal_ttl=3600;", "UPDATE CONFIGS storage:rocksdb_column_family_options = { disable_auto_compactions = True };"]
		for i in sql:
			commands.append(i)
		cmds = ""
		for i in commands:
			cmds += i + "\n"
		self.yaml = {
			"version":"v2",
			"description":"example",
			"removeTempFiles":False,
			"clientSettings":{
				"retry":3,
				"concurrency":concurrency,
				"channelBufferSize":1,
				"space":space,
				"connection":{
					"user":user,
					"password":password,
					"address":address
				},
				"postStart":{
					"commands":cmds,
					"afterPeriod":"8s"
				},
				"preStop":{
					"commands":"UPDATE CONFIGS storage:rocksdb_column_family_options = { disable_auto_compactions = False };\nUPDATE CONFIGS storage:wal_ttl=86400;"
				}
			},
			"logPath":"./err/test.log",
			"files":[file_yaml.file for file_yaml in files]
		}


	def save(self, filepath: str):
		print(f'保存在 {filepath}')
		yaml = YAML()
		with open(filepath, mode='w', encoding="utf-8") as f:
			yaml.dump(self.yaml, f)


if __name__ == '__main__':
	yaml = YAML()
	data = {
		"version":"v2",
		"description":"example",
		"removeTempFiles":False,
		"clientSettings":{
			"retry":3,
			"concurrency":1,
			"channelBufferSize":1,
			"space":"importer_test",
			"connection":{
				"user":"chengrong",
				"password":780128,
				"address":"127.0.0.1:9669"
			},
			"postStart":{
				"commands":"UPDATE CONFIGS storage:wal_ttl=3600;\nUPDATE CONFIGS storage:rocksdb_column_family_options = { disable_auto_compactions = True };\nDROP SPACE IF EXISTS importer_test;\nCREATE SPACE IF NOT EXISTS importer_test(partition_num=5, replica_factor=1, vid_type=int);\nUSE importer_test;\nCREATE TAG course(name string, credits int);\nCREATE TAG building(name string);\nCREATE TAG student(name string, age int, gender string);\nCREATE EDGE follow(likeness double);\nCREATE EDGE choose(grade int);\nCREATE TAG course_no_props();\nCREATE TAG building_no_props();\nCREATE EDGE follow_no_props();",
				"afterPeriod":"8s"
			},
			"preStop":{
				"commands":"UPDATE CONFIGS storage:rocksdb_column_family_options = { disable_auto_compactions = False };\nUPDATE CONFIGS storage:wal_ttl=86400;"
			}
		},
		"logPath":"./err/test.log",
		"files":[
			{
				"path":"./choose.csv",
				"batchSize":2,
				"inOrder":False,
				"type":"csv",
				"csv":{
					"withHeader":False,
					"withLabel":False
				},
				"schema":{
					"type":"edge",
					"edge":{
						"name":"choose",
						"withRanking":False,
						"srcVID":{
							"type":"int"
						},
						"dstVID":{
							"type":"int"
						},
						"props":[
							{
								"name":"grade",
								"type":"int"
							}
						]
					}
				}
			},
			{
				"path":"./course.csv",
				"failDataPath":"./err/course.csv",
				"batchSize":2,
				"inOrder":True,
				"type":"csv",
				"csv":{
					"withHeader":False,
					"withLabel":False
				},
				"schema":{
					"type":"vertex",
					"vertex":{
						"vid":{
							"type":"int"
						},
						"tags":[
							{
								"name":"course",
								"props":[
									{
										"name":"name",
										"type":"string"
									},
									{
										"name":"credits",
										"type":"int"
									}
								]
							},
							{
								"name":"building",
								"props":[
									{
										"name":"name",
										"type":"string"
									}
								]
							}
						]
					}
				}
			},
			{
				"path":"./course-with-header.csv",
				"failDataPath":"./err/course-with-header.csv",
				"batchSize":2,
				"inOrder":True,
				"type":"csv",
				"csv":{
					"withHeader":True,
					"withLabel":True
				},
				"schema":{
					"type":"vertex"
				}
			},
			{
				"path":"./follow-with-label.csv",
				"failDataPath":"./err/follow-with-label.csv",
				"batchSize":2,
				"inOrder":True,
				"type":"csv",
				"csv":{
					"withHeader":False,
					"withLabel":True
				},
				"schema":{
					"type":"edge",
					"edge":{
						"name":"follow",
						"withRanking":True,
						"srcVID":{
							"index":0,
							"type":"int"
						},
						"dstVID":{
							"index":2,
							"type":"int"
						},
						"rank":{
							"index":3
						},
						"props":[
							{
								"name":"likeness",
								"type":"double",
								"index":1
							}
						]
					}
				}
			},
			{
				"path":"./follow-with-label-and-str-vid.csv",
				"failDataPath":"./err/follow-with-label-and-str-vid.csv",
				"batchSize":2,
				"inOrder":True,
				"type":"csv",
				"csv":{
					"withHeader":False,
					"withLabel":True
				},
				"schema":{
					"type":"edge",
					"edge":{
						"name":"follow",
						"withRanking":True,
						"srcVID":{
							"index":0,
							"type":"int",
							"function":"hash"
						},
						"dstVID":{
							"index":2,
							"type":"int",
							"function":"hash"
						},
						"rank":{
							"index":3
						},
						"props":[
							{
								"name":"likeness",
								"type":"double",
								"index":1
							}
						]
					}
				}
			},
			{
				"path":"./follow.csv",
				"failDataPath":"./err/follow.csv",
				"batchSize":2,
				"type":"csv",
				"csv":{
					"withHeader":False,
					"withLabel":False
				},
				"schema":{
					"type":"edge",
					"edge":{
						"name":"follow",
						"withRanking":True,
						"srcVID":{
							"type":"int"
						},
						"dstVID":{
							"type":"int"
						},
						"props":[
							{
								"name":"likeness",
								"type":"double"
							}
						]
					}
				}
			},
			{
				"path":"./follow-with-header.csv",
				"failDataPath":"./err/follow-with-header.csv",
				"batchSize":2,
				"type":"csv",
				"csv":{
					"withHeader":True,
					"withLabel":False
				},
				"schema":{
					"type":"edge",
					"edge":{
						"name":"follow",
						"withRanking":True
					}
				}
			},
			{
				"path":"./student.csv",
				"failDataPath":"./err/student.csv",
				"batchSize":2,
				"type":"csv",
				"csv":{
					"withHeader":False,
					"withLabel":False
				},
				"schema":{
					"type":"vertex",
					"vertex":{
						"vid":{
							"type":"int"
						},
						"tags":[
							{
								"name":"student",
								"props":[
									{
										"name":"name",
										"type":"string"
									},
									{
										"name":"age",
										"type":"int"
									},
									{
										"name":"gender",
										"type":"string"
									}
								]
							}
						]
					}
				}
			},
			{
				"path":"./student.csv",
				"failDataPath":"./err/student_index.csv",
				"batchSize":2,
				"type":"csv",
				"csv":{
					"withHeader":False,
					"withLabel":False
				},
				"schema":{
					"type":"vertex",
					"vertex":{
						"vid":{
							"index":1,
							"function":"hash"
						},
						"tags":[
							{
								"name":"student",
								"props":[
									{
										"name":"age",
										"type":"int",
										"index":2
									},
									{
										"name":"name",
										"type":"string",
										"index":1
									},
									{
										"name":"gender",
										"type":"string"
									}
								]
							}
						]
					}
				}
			},
			{
				"path":"./student-with-label-and-str-vid.csv",
				"failDataPath":"./err/student_label_str_vid.csv",
				"batchSize":2,
				"type":"csv",
				"csv":{
					"withHeader":False,
					"withLabel":True
				},
				"schema":{
					"type":"vertex",
					"vertex":{
						"vid":{
							"index":1,
							"function":"hash",
							"type":"int"
						},
						"tags":[
							{
								"name":"student",
								"props":[
									{
										"name":"age",
										"type":"int",
										"index":2
									},
									{
										"name":"name",
										"type":"string",
										"index":1
									},
									{
										"name":"gender",
										"type":"string"
									}
								]
							}
						]
					}
				}
			},
			{
				"path":"./follow.csv",
				"failDataPath":"./err/follow_index.csv",
				"batchSize":2,
				"limit":3,
				"type":"csv",
				"csv":{
					"withHeader":False,
					"withLabel":False
				},
				"schema":{
					"type":"edge",
					"edge":{
						"name":"follow",
						"srcVID":{
							"index":0,
							"type":"int"
						},
						"dstVID":{
							"index":1,
							"type":"int"
						},
						"rank":{
							"index":2
						},
						"props":[
							{
								"name":"likeness",
								"type":"double",
								"index":3
							}
						]
					}
				}
			},
			{
				"path":"./follow-delimiter.csv",
				"failDataPath":"./err/follow-delimiter.csv",
				"batchSize":2,
				"type":"csv",
				"csv":{
					"withHeader":True,
					"withLabel":False,
					"delimiter":"|"
				},
				"schema":{
					"type":"edge",
					"edge":{
						"name":"follow",
						"withRanking":True
					}
				}
			},
			{
				"path":"https://raw.githubusercontent.com/vesoft-inc/nebula-importer/master/examples/v2/follow.csv",
				"failDataPath":"./err/follow_http.csv",
				"batchSize":2,
				"limit":3,
				"type":"csv",
				"csv":{
					"withHeader":False,
					"withLabel":False
				},
				"schema":{
					"type":"edge",
					"edge":{
						"name":"follow",
						"srcVID":{
							"index":0,
							"function":"hash",
							"type":"int"
						},
						"dstVID":{
							"index":1,
							"function":"hash",
							"type":"int"
						},
						"rank":{
							"index":2
						},
						"props":[
							{
								"name":"likeness",
								"type":"double",
								"index":3
							}
						]
					}
				}
			},
			{
				"path":"./course.csv",
				"failDataPath":"./err/course-empty-props.csv",
				"batchSize":2,
				"inOrder":True,
				"type":"csv",
				"csv":{
					"withHeader":False,
					"withLabel":False,
					"delimiter":","
				},
				"schema":{
					"type":"vertex",
					"vertex":{
						"vid":{
							"index":0,
							"type":"int"
						},
						"tags":[
							{
								"name":"course_no_props"
							}
						]
					}
				}
			},
			{
				"path":"./course.csv",
				"failDataPath":"./err/course-multi-empty-props.csv",
				"batchSize":2,
				"inOrder":True,
				"type":"csv",
				"csv":{
					"withHeader":False,
					"withLabel":False,
					"delimiter":","
				},
				"schema":{
					"type":"vertex",
					"vertex":{
						"vid":{
							"index":0,
							"type":"int"
						},
						"tags":[
							{
								"name":"course_no_props"
							},
							{
								"name":"building_no_props"
							}
						]
					}
				}
			},
			{
				"path":"./course.csv",
				"failDataPath":"./err/course-mix-empty-props.csv",
				"batchSize":2,
				"inOrder":True,
				"type":"csv",
				"csv":{
					"withHeader":False,
					"withLabel":False,
					"delimiter":","
				},
				"schema":{
					"type":"vertex",
					"vertex":{
						"vid":{
							"index":0,
							"type":"int"
						},
						"tags":[
							{
								"name":"course_no_props"
							},
							{
								"name":"building",
								"props":[
									{
										"name":"name",
										"type":"string",
										"index":3
									}
								]
							}
						]
					}
				}
			},
			{
				"path":"./course.csv",
				"failDataPath":"./err/course-mix-empty-props-2.csv",
				"batchSize":2,
				"inOrder":True,
				"type":"csv",
				"csv":{
					"withHeader":False,
					"withLabel":False,
					"delimiter":","
				},
				"schema":{
					"type":"vertex",
					"vertex":{
						"vid":{
							"index":0,
							"type":"int"
						},
						"tags":[
							{
								"name":"building",
								"props":[
									{
										"name":"name",
										"type":"string",
										"index":3
									}
								]
							},
							{
								"name":"course_no_props"
							}
						]
					}
				}
			},
			{
				"path":"./follow.csv",
				"failDataPath":"./err/follow-empty-props.csv",
				"batchSize":2,
				"type":"csv",
				"csv":{
					"withHeader":False,
					"withLabel":False,
					"delimiter":","
				},
				"schema":{
					"type":"edge",
					"edge":{
						"name":"follow_no_props",
						"withRanking":False,
						"dstVID":{
							"index":1,
							"type":"int"
						},
						"srcVID":{
							"index":0,
							"type":"int"
						}
					}
				}
			},
			{
				"path":"./choose-hex.csv",
				"batchSize":2,
				"inOrder":False,
				"type":"csv",
				"csv":{
					"withHeader":False,
					"withLabel":False
				},
				"schema":{
					"type":"edge",
					"edge":{
						"name":"choose",
						"withRanking":False,
						"srcVID":{
							"index":0,
							"type":"int"
						},
						"dstVID":{
							"index":1,
							"type":"int"
						},
						"props":[
							{
								"name":"grade",
								"type":"int",
								"int":2
							}
						]
					}
				}
			},
			{
				"path":"./choose-hex.csv",
				"batchSize":2,
				"inOrder":False,
				"type":"csv",
				"csv":{
					"withHeader":False,
					"withLabel":False
				},
				"schema":{
					"type":"edge",
					"edge":{
						"name":"choose",
						"withRanking":False,
						"srcVID":{
							"index":0,
							"type":"int"
						},
						"dstVID":{
							"index":1,
							"type":"int"
						},
						"props":[
							{
								"name":"grade",
								"type":"int",
								"int":2
							}
						]
					}
				}
			}
		]
	}

	with open('qwq.yaml', mode='w', encoding="utf-8") as f:
		yaml.dump(data, f)