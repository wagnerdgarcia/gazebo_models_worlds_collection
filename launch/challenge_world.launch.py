import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, SetEnvironmentVariable, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    # --- Identifica o pacote onde este launch file está ---
    # (Assumindo que o pacote se chama 'challenge_simulation')
    pkg_challenge_share = get_package_share_directory('challenge_simulation')
    pkg_uav_share = get_package_share_directory('laser_uav_simulation')
    
    # --- Define o caminho para o arquivo de mundo ---
    # world_path = os.path.join(pkg_challenge_share, 'worlds', 'small_city.world')
    world_path = os.path.join(pkg_challenge_share, 'worlds', 'outdoor.world')
    
    # --- 1. LOCALIZA O ARQUIVO DE PARÂMETROS ---
    # Esta linha encontra o arquivo 'gazebo_params.yaml' dentro da pasta 'params' do seu pacote.
    params_file_path = os.path.join(pkg_challenge_share, 'params', 'gazebo_params.yaml')
    
    # --- Define os caminhos dos modelos (sem alterações) ---
    challenge_models_path = os.path.join(pkg_challenge_share, 'models')
    uav_models_path = os.path.join(pkg_uav_share, 'models')
    if 'GAZEBO_MODEL_PATH' in os.environ:
        gazebo_models_path = os.environ['GAZEBO_MODEL_PATH'] + ':' + challenge_models_path + ':' + uav_models_path
    else:
        gazebo_models_path = challenge_models_path + ':' + uav_models_path

    set_gazebo_model_path = SetEnvironmentVariable(
        name='GAZEBO_MODEL_PATH',
        value=gazebo_models_path
    )
    
    # --- Declare launch argument for world ---
    declare_world_arg = DeclareLaunchArgument(
        'world',
        default_value=world_path,
        description='Path to the world file'
    )
    
    # --- 2. ATUALIZA O COMANDO PARA USAR O ARQUIVO DE PARÂMETROS ---
    # Ação para iniciar o Gazebo Server
    start_gazebo_cmd = ExecuteProcess(
        cmd=['gazebo', '--verbose', LaunchConfiguration('world'),
             '-s', 'libgazebo_ros_init.so',
             '-s', 'libgazebo_ros_factory.so', 
            
            '--ros-args',
            '--param', 'publish_rate:=1000.0'
        ],
        output='screen'
    )


    return LaunchDescription([
        declare_world_arg,
        set_gazebo_model_path,
        start_gazebo_cmd,
    ])