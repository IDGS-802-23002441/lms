using Microsoft.AspNetCore.Mvc;
using Npgsql;

namespace ApiSensores.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class SensoresController : ControllerBase
    {
        private readonly string connectionString;

        public SensoresController(IConfiguration configuration)
        {
            connectionString = configuration.GetConnectionString("Postgres")
                ?? throw new InvalidOperationException("Connection string 'Postgres' was not found.");
        }

        [HttpPost]
        public async Task<IActionResult> GuardarLectura([FromBody] Lectura lectura)
        {
            var builder = new NpgsqlConnectionStringBuilder(connectionString);
            Console.WriteLine($"DB host: {builder.Host}");

            using var conn =
                new NpgsqlConnection(connectionString);

            await conn.OpenAsync();

            string sql =
                @"INSERT INTO lecturas(sensor, valor)
                  VALUES(@sensor, @valor)";

            using var cmd =
                new NpgsqlCommand(sql, conn);

            cmd.Parameters.AddWithValue("sensor", lectura.Sensor);
            cmd.Parameters.AddWithValue("valor", lectura.Valor);

            await cmd.ExecuteNonQueryAsync();

            return Ok(new
            {
                mensaje = "Lectura guardada"
            });
        }
    

       [HttpGet]
public async Task<IActionResult> ObtenerLecturas()
{
    using var conn = new NpgsqlConnection(connectionString);
    await conn.OpenAsync();

    // Solicitamos explícitamente las 4 columnas de la tabla en un orden estricto
    string sql = @"SELECT id, sensor, valor, fecha FROM lecturas ORDER BY fecha DESC";
    
    using var cmd = new NpgsqlCommand(sql, conn);
    using var reader = await cmd.ExecuteReaderAsync();
    
    var lista = new List<object>();
    while (await reader.ReadAsync())
    {
        // Evaluamos cada columna según el tipo de dato que reportó tu error anterior
        string idFila = reader.IsDBNull(0) ? "" : reader.GetString(0); // Alfanumérico (varchar)
        string sensorFila = reader.IsDBNull(1) ? "" : reader.GetString(1);
        double valorFila = reader.IsDBNull(2) ? 0.0 : reader.GetDouble(2);
        
        // Manejo de fecha flexible (si es timestamp u objeto, usamos GetValue y lo volvemos string)
        string fechaFila = reader.IsDBNull(3) ? "" : reader.GetValue(3)?.ToString() ?? "";

        lista.Add(new
        {
            id = idFila,
            sensor = sensorFila,
            valor = valorFila,
            fecha = fechaFila
        });
    }

    return Ok(lista);
}
    }
    public class Lectura
    {
        public string Sensor { get; set; } = "";
        public double Valor { get; set; }
    }
}