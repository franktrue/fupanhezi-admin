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
          width: 140,
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
          }
      },
      indexRow: false,
      viewOptions: {
          componentType: "form"
      },
      formOptions: {
          defaultSpan: 24, // 默认的表单 span
          width: "35%"
      },
      indexRow: { // 或者直接传true,不显示title，不居中
        title: '序号',
        align: 'center',
        width: 60
      },
      columns: [
        {
          title: "交易日期",
          key: "trade_date",
          type: "date",
          search: {
            component: {
              props: {
                format: 'yyyy-MM-dd',
                valueFormat: 'yyyy-MM-dd'
              }
            }
          },
          form: {
            rules: [
              { required: true, message: "交易日期必填" }
            ],
            component: {
              props: {
                clearable: true,
                format: 'yyyy-MM-dd',
                valueFormat: 'yyyy-MM-dd'
              },
              placeholder: "请输入交易日期"
            }
          }
        }
      ]
  };
};
