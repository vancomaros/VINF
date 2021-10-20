import re
import datetime


def replace_dates(template):
    next_template = template.find("{{")
    if next_template != -1:
        date = datetime.datetime.now()
        template = template.replace("{{CURRENTYEAR}}", str(date.year))
        template = template.replace("{{CURRENTMONTH}}", str(date.month))
        template = template.replace("{{CURRENTWEEK}}", str(date.strftime("%W")))
        template = template.replace("{{CURRENTDAY}}", str(date.day))
    return template


def add_dict(template, dictionary):
    if template in dictionary:
        dictionary[template] += 1
    else:
        dictionary[template] = 1


def remove_brackets(template):
    return template[2:-2]


def get_parameters(template, parameters_dict):
    parameter_index = template.find("|")
    if parameter_index != -1:
        parameters = template.split("|")
        if not (parameters[0] in parameters_dict):
            parameters_dict[parameters[0]] = []
        for parameter in parameters[1:]:
            variable = parameter.split("=")[0]
            if not (variable in parameters_dict[parameters[0]]):
                parameters_dict[parameters[0]].append(variable)
        template = template[:parameter_index + 1]


def main():
    templates_dict = {}
    parameters_dict = {}
    t = 1
    flag = 0
    line_groups = []

    with open('out.xml', encoding="utf8") as wiki:
        for line in wiki:
            t += 1
            templates = []

            if line.count("{{") > line.count("}}"):
                line = line.replace("\n", "")
                line_groups.append(line)
                flag += line.count("{{")
                flag -= line.count("}}")
                continue

            elif flag:
                line = line.replace("\n", "")
                line_groups.append(line)

                if line.count("}}") > line.count("{{"):
                    flag -= line.count("}}")
                    flag += line.count("{{")
                    if flag == 0:
                        line = "".join(line_groups)
                        line_groups = []
                    else:
                        continue
                else:
                    continue

            templates = re.findall("\{\{(?:[^}}{{]+|\{\{(?:[^}}{{]+|\{\{[^}}{{]*\}\})*\}\})*\}\}", line)
            if len(templates) != 0:
                for template in templates:
                    template = remove_brackets(template)
                    template = replace_dates(template)
                    get_parameters(template, parameters_dict)

                    # print(template, t)
                    add_dict(template.split("|")[0], templates_dict)

#                        if t > 47570:
#                            print(line)

#                if t == 47570:
#                   break
        print(parameters_dict)
        print(dict(sorted(templates_dict.items(), key=lambda item: item[1], reverse=True)))


main()
