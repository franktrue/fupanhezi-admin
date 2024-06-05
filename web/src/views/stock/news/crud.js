export const crudOptions = vm => {
  return {
      pageOptions: {
          compact: true
      },
      options: {
          tableType: "vxe-table",
          rowKey: true, // 必须设置，true or false
          rowId: "id",
          height: "100%", // 表格高度100%, 使用toolbar必须设置
          highlightCurrentRow: false
      },
      rowHandle: {
          width: 240,
          view: {
              thin: true,
              text: "",
              disabled() {
                  return !vm.hasPermissions("Retrieve");
              }
          },
          edit: {
              thin: true,
              text: "",
              disabled() {
                  return !vm.hasPermissions("Update");
              }
          },
          remove: {
              thin: true,
              text: "",
              disabled() {
                  return !vm.hasPermissions("Delete");
              }
          },
          custom: [{
            text: '题材',
            type: 'success',
            size: 'small',
            icon: 'el-icon-folder',
            emit: 'newsTag'
          }]
      },
      indexRow: { // 或者直接传true,不显示title，不居中
        title: '序号',
        align: 'center',
        width: 80
      },
      viewOptions: {
          componentType: "form"
      },
      formOptions: {
          defaultSpan: 24, // 默认的表单 span
          width: "60%"
      },
      columns: [
          {
            title: '标题',
            key: 'title',
            search: {
              component: {
                props: {
                  clearable: true
                }
              }
            },
            form: {
              component: {
                props: {
                  clearable: true
                }
              },
              rules: [{ required: true, message: '标题必填' }]
            }
          },
          {
            title: '内容',
            key: 'content',
            type: 'editor-wang',
            show: false,
            form: {
              component: {
                props: {
                  clearable: true
                }
              },
              rules: [{ required: true, message: '股票名称必填' }]
            }
          },
          {
            title: '类型',
            key: 'type',
            type: 'radio',
            dict: {
              data: vm.dictionary('news_type')
            },
            form: {
              value: "topic",
              component: {
                props: {
                  clearable: true
                }
              },
              helper: "“题材”类型需完善后发布"
            }
          },
          {
            title: '板块',
            key: 'board',
            show: false,
            type: 'select',
            dict: {
              url(dict,{form,component}){
                console.log(form)
                return '/api/stock/news/boards/'
              },
              cache: false,
            },
            form: {
              component: {
                show (context) {
                  const { form } = context
                  return form.type == "board"
                },
                props: {
                  elProps:{
                    filterable: true,
                    multiple: false,
                    clearable: true
                  },
                },
              }
            },
          },
          {
            title: '标签',
            key: 'tags',
            show: false,
            form: {
              component: {
                props: {
                  clearable: true
                }
              },
              helper: "请使用,隔开"
            }
          },
          {
            title: '发布',
            key: 'status',
            type: 'dict-switch',
            dict: {
              data: vm.dictionary('button_whether_number')
            },
            form: {
              value: 0,
              component: {
                props: {
                  clearable: true
                }
              },
              helper: "下架后不可用"
            }
          },
          {
            title: '排序',
            key: 'sort',
            type: 'number',
            sortable: 'custom',
            form: {
              value: 0,
              component: {
                props: {
                  clearable: true
                }
              }
            }
          },
      ]
  };
};
