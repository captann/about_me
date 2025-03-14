import json
import matplotlib.pyplot as plt
import datetime
from PIL import Image
import os

def convert_to_pdf(graphics_folder="main/graphics", pdf_folder="main/pdf", name='res.pdf', gi=True):
    if gi:
        images = [
            Image.open(os.path.abspath(
                os.path.curdir) + '/' + graphics_folder + '/' + f + '/' +
                       os.listdir(os.path.abspath(
                           os.path.curdir) + '/' + graphics_folder + '/' + f)[
                           0]).convert("RGB")
            for f in sorted(os.listdir(graphics_folder))
        ]
        pdf_path = pdf_folder + '/' + name
        images[0].save(
            pdf_path, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:]
        )

    else:
        images = [
            Image.open(os.path.abspath(
                os.path.curdir) + '/' + graphics_folder + '/' + f + '/' +
                       os.listdir(os.path.abspath(
                           os.path.curdir) + '/' + graphics_folder + '/' + f)[
                           0]).convert("RGB")
            for f in sorted([i for i in os.listdir(graphics_folder) if i != 'gi_bp_meds'])
        ]
        pdf_path = pdf_folder + '/' + name
        images[0].save(
            pdf_path, "PDF", resolution=100.0, save_all=True,
            append_images=images[1:]
        )
    return pdf_path

class Config:
    max_weight = 15
    keys = ['date', 'gi_meds_taken', 'bp_meds_taken', 'hand_exercise_weight']

def write_file(decay_coefficient, weights_file, data_folder, output_dir,
               graphics_folder, pdf_folder, gi=True):
    os.makedirs(graphics_folder, exist_ok=True)
    os.makedirs(data_folder, exist_ok=True)
    os.makedirs(pdf_folder, exist_ok=True)

    # Загрузка весовых коэффициентов из JSON файла
    with open(weights_file, 'r') as f:
        weights = json.load(f)

    # Словарь для хранения данных
    data = {}
    # Загрузка данных из файлов JSON
    for key in Config.keys:
        file_path = os.path.join(data_folder, f"{key}.json")
        with open(file_path, 'r') as f:
            data[key] = json.load(f)
    dates = data['date']
    # Пример настройки для курсов
    with open(f"{data_folder}/total_tasks.json", "r") as f:
        total_tasks = json.load(f)
    total_tasks_sa = total_tasks['total_tasks_sa']
    total_tasks_dc = total_tasks['total_tasks_dc']
    total_tasks_nir = total_tasks['total_tasks_nir']

    # Загрузка tasks_completed
    with open(f"{data_folder}/tasks_completed.json", "r") as f:
        tasks_completed_data = json.load(f)
    tasks_completed_sa = (tasks_completed_data['tasks_completed_sa'])
    tasks_completed_dc = (tasks_completed_data['tasks_completed_dc'])
    tasks_completed_nir = (tasks_completed_data['tasks_completed_nir'])

    # Инициализация списков для хранения значений
    cumulative_tasks_sa = []
    sa_course_progress = []
    cumulative_tasks_dc = []
    digital_course_progress = []
    cumulative_tasks_nir = []
    nir_course_progress = []
    efficiency_sa = []
    efficiency_dc = []
    efficiency_nir = []
    daily_progress = []
    gi_meds_taken = data['gi_meds_taken']
    bp_meds_taken = data['bp_meds_taken']
    hand_exercise_weight = data['hand_exercise_weight']

    cumulative_sum_sa = 0
    cumulative_sum_dc = 0
    cumulative_sum_nir = 0
    prev_daily_progress = 0

    for i in range(len(gi_meds_taken)):
        cumulative_sum_sa += tasks_completed_sa[i]
        cumulative_sum_dc += tasks_completed_dc[i]
        cumulative_sum_nir += tasks_completed_nir[i]

        cumulative_tasks_sa.append(cumulative_sum_sa)
        cumulative_tasks_dc.append(cumulative_sum_dc)
        cumulative_tasks_nir.append(cumulative_sum_nir)

        sa_course_progress.append(cumulative_sum_sa / total_tasks_sa)
        digital_course_progress.append(cumulative_sum_dc / total_tasks_dc)
        nir_course_progress.append(cumulative_sum_nir / total_tasks_nir)

        efficiency_sa_value = (tasks_completed_sa[i] / total_tasks_sa)
        efficiency_dc_value = (tasks_completed_dc[i] / total_tasks_dc)
        efficiency_nir_value = (tasks_completed_nir[i] / total_tasks_nir )

        efficiency_sa.append(efficiency_sa_value)
        if len(efficiency_sa) > 1:
            if efficiency_sa[-2] == 0:
                efficiency_sa[-1] *= decay_coefficient
        efficiency_dc.append(efficiency_dc_value)
        if len(efficiency_dc) > 1:
            if efficiency_dc[-2] == 0:
                efficiency_dc[-1] *= decay_coefficient
        efficiency_nir.append(efficiency_nir_value)
        if len(efficiency_nir) > 1:
            if efficiency_nir[-2] == 0:
                efficiency_nir[-1] *= decay_coefficient


        TABLET_COEFFICIENT = 0.2
        prev_daily_progress = daily_progress[-1] if daily_progress else 0
        daily_progress_value = (weights['gi_meds_taken'] * gi_meds_taken[i]  * TABLET_COEFFICIENT +
                                weights['bp_meds_taken'] * bp_meds_taken[i] * TABLET_COEFFICIENT +
                                weights['hand_exercise_weight'] * (
                                            hand_exercise_weight[
                                                i] / Config.max_weight) +
                                weights['digital_course_progress'] *
                                efficiency_dc[-1] +
                                weights['sa_course_progress'] *
                                efficiency_sa[-1] +
                                weights['nir_course_progress'] *
                                efficiency_nir[-1])
        daily_progress.append(daily_progress_value if prev_daily_progress else daily_progress_value * decay_coefficient)

    # Создание графиков
    time = str(datetime.date.today() - datetime.timedelta(days=1))
    def save_plot(fig, title, folder_name):
        # Создаем папку для каждого графика
        folder_path = os.path.join(output_dir, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        # Сохраняем график
        fig.savefig(os.path.join(folder_path, f"{title}.png"))
        plt.close(fig)  # Закрываем фигуру после сохранения


    # График для ЖКТ и таблеток от давления
    fig1, axs1 = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    x = dates  # Предполагается, что даты хранятся в списке dates
    # График для ЖКТ
    axs1[0].step(x, gi_meds_taken, label="Прием таблеток для ЖКТ (0-1)",
                 where='post', color='blue', marker='o',
                 markerfacecolor='magenta')
    axs1[0].set_title("Прием таблеток для ЖКТ " + time)
    axs1[0].grid(True, which='both', linestyle='--', linewidth=0.5)
    axs1[0].set_yticks(list(set(gi_meds_taken)))  # Уникальные значения из данных
    axs1[0].set_xticks(x)

    # График для таблеток от давления
    axs1[1].step(x, bp_meds_taken, label="Прием таблеток от давления (0-1)",
                 where='post', color='green', marker='o',
                 markerfacecolor='magenta')
    axs1[1].set_title("Прием таблеток от давления " + time)
    axs1[1].grid(True, which='both', linestyle='--', linewidth=0.5)

    axs1[1].set_xlabel("День")
    axs1[1].set_yticks(list(set(bp_meds_taken))) # Уникальные значения из данных
    axs1[1].set_xticks(x)
    save_plot(fig1, 'Медикаменты', 'gi_bp_meds')

    # Графики для курсов
    fig2, axs2 = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    axs2[0].plot(x, sa_course_progress,
                 label="Прогресс по курсу системной аналитики", color='purple',
                 marker='o', markerfacecolor='magenta')
    axs2[0].set_title("Прогресс по курсу системной аналитики " + time)
    axs2[0].grid(True, which='both', linestyle='--', linewidth=0.5)

    axs2[0].set_yticks(list(set(sa_course_progress)))  # Уникальные значения из данных
    axs2[0].set_xticks(x)

    axs2[1].plot(x, efficiency_sa,
                 label="Эффективность по курсу системной аналитики",
                 color='cyan', marker='o', markerfacecolor='magenta')
    axs2[1].set_title("Эффективность по курсу системной аналитики " + time)
    axs2[1].grid(True, which='both', linestyle='--', linewidth=0.5)

    axs2[1].set_xlabel("День")

    axs2[1].set_yticks(list(set(efficiency_sa)))  # Уникальные значения из данных
    axs2[1].set_xticks(x)
    save_plot(fig2, 'Курс системной аналитики', 'system_analysis')

    fig3, axs3 = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    axs3[0].plot(x, digital_course_progress,
                 label="Прогресс по курсу цифровой кафедры", color='orange',
                 marker='o', markerfacecolor='magenta')
    axs3[0].set_title("Прогресс по курсу цифровой кафедры " + time)
    axs3[0].grid(True, which='both', linestyle='--', linewidth=0.5)

    axs3[0].set_yticks(list(set(digital_course_progress)))  # Уникальные значения из данных
    axs3[0].set_xticks(x)

    axs3[1].plot(x, efficiency_dc,
                 label="Эффективность по курсу цифровой кафедры",
                 color='brown', marker='o', markerfacecolor='magenta')
    axs3[1].set_title("Эффективность по курсу цифровой кафедры " + time)
    axs3[1].grid(True, which='both', linestyle='--', linewidth=0.5)

    fig6, axs6 = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    axs6[0].plot(x, nir_course_progress,
                 label="Прогресс по научно-исследовательской работе", color='orange',
                 marker='o', markerfacecolor='magenta')
    axs6[0].set_title("Прогресс по научно-исследовательской работе " + time)
    axs6[0].grid(True, which='both', linestyle='--', linewidth=0.5)

    axs6[0].set_yticks(
        list(set(nir_course_progress)))  # Уникальные значения из данных
    axs6[0].set_xticks(x)

    axs6[1].plot(x, efficiency_nir,
                 label="Эффективность по научно-исследовательской работе",
                 color='brown', marker='o', markerfacecolor='magenta')
    axs6[1].set_title("Эффективность по научно-исследовательской работе " + time)
    axs6[1].grid(True, which='both', linestyle='--', linewidth=0.5)

    axs6[1].set_xlabel("День")
    axs6[1].set_yticks(
        list(set(efficiency_nir)) ) # Уникальные значения из данных
    axs6[1].set_xticks(x)
    save_plot(fig6, 'Научно-исследовательская работа', 'nir')

    # График для веса гантелей по дням
    fig5, ax5 = plt.subplots(figsize=(10, 5))
    ax5.plot(x, hand_exercise_weight, label="Вес гантелей для упражнений",
             color='cyan', marker='o', markerfacecolor='magenta')
    ax5.set_title("Прогресс веса гантелей для упражнений " + time)
    ax5.set_xlabel("День")
    ax5.set_ylabel("Вес гантелей (кг)")
    ax5.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax5.set_yticks(
        list(set(hand_exercise_weight)))  # Уникальные значения из данных
    ax5.set_xticks(x)
    save_plot(fig5, 'Вес гантелей', 'hand_weights')

    # График для совокупного прогресса
    fig4, ax4 = plt.subplots(figsize=(10, 5))
    ax4.plot(x, daily_progress, label="Совокупный прогресс", color='brown',
             marker='o', markerfacecolor='magenta')
    ax4.set_title("Общая эффективность " + time)
    ax4.set_xlabel("День")
    ax4.grid(True, which='both', linestyle='--', linewidth=0.5)

    ax4.set_yticks(
        list(set(daily_progress))) # Уникальные значения из данных
    ax4.set_xticks(x)
    save_plot(fig4, 'Общая эффективность', 'total_efficiency')

    return convert_to_pdf(graphics_folder=graphics_folder,
                          pdf_folder=pdf_folder,
                          name=time + ' ' + str(int(gi)) + '.pdf', gi=gi)



if __name__ == "__main__":
    pass
