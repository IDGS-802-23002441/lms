using System.ComponentModel.DataAnnotations.Schema;

namespace ApiSensores.Models
{
    [Table("lecturas")]
    public class Lectura
    {
        public int id { get; set; }

        public string sensor { get; set; } = "";

        public double valor { get; set; }

        public DateTime fecha { get; set; } = DateTime.UtcNow;
    }
}