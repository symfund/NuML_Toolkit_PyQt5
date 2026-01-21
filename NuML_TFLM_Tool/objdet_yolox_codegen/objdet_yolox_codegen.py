import os

from objdet_yolox_codegen.YoloXnanoNu_hpp_codegen import YoloXnanoNuHppCodegen
from objdet_yolox_codegen.YoloXnanoNu_cpp_codegen import YoloXnanoNuCppCodegen
from objdet_yolox_codegen.Labels_cpp_codegen import LabelsCppCodegen
from objdet_yolox_codegen.main_cpp_codegen import MainCCodegen

class ObjDetYoloXCodegen:
    def __init__(self, model, project, vela_summary, **kwargs):
        self.model = model
        self.project = project
        self.vela_summary = vela_summary
        self.extra = kwargs

    @classmethod
    def from_args(cls, *args, **kwargs):
        return cls(*args, **kwargs)
    
    def code_gen(self):
        print('Run object detection codegen for YOLOX nano...')
        print(f"model:{self.model}")
        print(f"project:{self.project}")
        for key, value in self.extra.items():
            print(f"extra param:{key}, {value}")

        template_path = 'objdet_yolox_codegen'

        #Generate YoloXnanoNu.hpp file
        NNModel_hpp_file_path = os.path.join(self.project, 'Model', 'include', 'YoloXnanoNu.hpp')
        NNModel_hpp_temp_file_path = os.path.join(template_path, 'YoloXnanoNu_hpp_tmpl.jinja2')
        print(f'YoloXnanoNu.hpp template path {NNModel_hpp_temp_file_path}')
        print(f'YoloXnanoNu.hpp file path {NNModel_hpp_file_path}')

        try:
            NNModel_hpp_file = open(NNModel_hpp_file_path, "w")
        except OSError:
            print("Could not open YoloXnanoNu.hpp file")
            return 'unable_generate'

        with NNModel_hpp_file:
            NNModel_hpp_codegen = YoloXnanoNuHppCodegen()
            NNModel_hpp_codegen.code_gen(NNModel_hpp_file, NNModel_hpp_temp_file_path, self.model)

        #Generate YoloXnanoNu.cpp.cpp file
        NNModel_cpp_file_path = os.path.join(self.project, 'Model', 'YoloXnanoNu.cpp')
        NNModel_cpp_temp_file_path = os.path.join(template_path, 'YoloXnanoNu_cpp_tmpl.jinja2')
        print(f'YoloXnanoNu.cpp template path {NNModel_cpp_temp_file_path}')
        print(f'YoloXnanoNu.cpp file path {NNModel_cpp_file_path}')

        try:
            NNModel_cpp_file = open(NNModel_cpp_file_path, "w")
        except OSError:
            print("Could not open YoloXnanoNu.cpp file")
            return 'unable_generate'

        with NNModel_cpp_file:
            NNModel_cpp_codegen = YoloXnanoNuCppCodegen()
            NNModel_cpp_codegen.code_gen(NNModel_cpp_file, NNModel_cpp_temp_file_path, self.model)

        #Generate Labels.cpp file
        Labels_cpp_file_path = os.path.join(self.project, 'Model', 'Labels.cpp')
        Labels_cpp_temp_file_path = os.path.join(template_path, 'Labels_cpp_tmpl.jinja2')
        print(f'Labels.cpp template path {Labels_cpp_temp_file_path}')
        print(f'Labels.cpp file path {Labels_cpp_file_path}')

        try:
            Lables_cpp_file = open(Labels_cpp_file_path, "w")
        except OSError:
            print("Could not open Labels.cpp file")
            return 'unable_generate'

        with Lables_cpp_file:
            Labels_codegen = LabelsCppCodegen()
            Labels_codegen.code_gen(Lables_cpp_file, Labels_cpp_temp_file_path, self.model)

        #Generate main.cpp file
        main_file_path = os.path.join(self.project, 'main.cpp')
        main_temp_file_path = os.path.join(template_path, 'main_cpp_tmpl.jinja2')
        print(f'template path {main_temp_file_path}')
        print(f'main file path {main_file_path}')

        try:
            main_file = open(main_file_path, "w")
        except OSError:
            print("Could not open main file")
            return 'unable_generate'

        with main_file:
            main_codegen = MainCCodegen()
            main_codegen.code_gen(main_file, main_temp_file_path, self.vela_summary)